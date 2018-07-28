from simso.core import Scheduler, Timer
from simso.core.Task import PTask
from simso.schedulers import scheduler


@scheduler("simso.schedulers.EDF_CBS")
class EDF_CBS(Scheduler):
    def is_soft_job(self, job):
        return self.is_soft_task(job.task)

    def is_soft_task(self, task):
        return task.data['soft']

    def init(self):
        self.ready_list = []
        # Create CBS servers for each soft task
        list_servers = []
        self.soft_task_list = []
        for task in self.task_list:
            if self.is_soft_task(task):
                list_servers.append(CBSServer(task, task.data['cbs_period'],
                                              task.data['cbs_maximum_runtime'],
                                              task.data['cbs_deadline']))
                self.soft_task_list.append(task)

        self.cbs_servers = dict(zip(self.soft_task_list, list_servers))

    def on_activate(self, job):

        # CBS
        if self.is_soft_job(job):
            server = self.cbs_servers[job.task]

            # If the ready list of the server is empty new runtime and deadline are computed and
            # the deadline_timer is started
            if (not server.ready_list):
                # qi < (di - t)Qi/Ti
                if not (server.current_runtime <
                        (server.current_deadline - self.sim.now_ms())
                        * (server.maximum_runtime / server.deadline)):
                    # d = t + D, q = Q
                    self.cbs_servers[job.task].set(self.cbs_servers[job.task].maximum_runtime,
                                                   self.sim.now_ms() + self.cbs_servers[job.task].deadline,
                                                   self.sim.now_ms(),
                                                   Timer(self.sim, EDF_CBS.deadline_call,
                                                         (self, self.cbs_servers[job.task]),
                                                         self.cbs_servers[job.task].deadline, one_shot=True,
                                                         cpu=self.processors[0], overhead=.000))
            # The job is added to the ready_list of the server
            server.add_job(job)
        else:  # EDF
            self.ready_list.append(job)

        job.cpu.resched()

    def on_terminated(self, job):
        # CBS
        if self.is_soft_job(job):
            server = self.cbs_servers[job.task]
            # The job is removed from the ready_list of the server
            server.remove_job(job)
        # EDF
        else:
            self.ready_list.remove(job)

        job.cpu.resched()

    def schedule(self, cpu):
        # update runtime of the running server on cpu if exists

        if cpu.running and self.is_soft_job(cpu.running):
            self.cbs_servers[cpu.running.task].update_runtime(self.sim.now_ms())

        key = lambda x: (
            1 if not x.running else 0,
            self.cbs_servers[x.running.task].current_deadline if x.running and self.is_soft_job(x.running) else
                x.running.absolute_deadline if x.running else 0,
            1 if x is cpu else 0
        )
        cpu_min = max(self.processors, key=key)
        # cpu_min = cpu

        hard_job = None
        l = [j for j in self.ready_list if j.is_active() and not j.is_running()]
        if l:
            hard_job = min(l, key=lambda x: x.absolute_deadline)

        # List of CBS servers with a ready job which is not currently running
        ready_servers = [s for s in self.cbs_servers.values()
                         if s.ready_list
                         and not s.ready_list[0].is_running()
                         and not s.is_throttled
                         ]

        # Choose the job-server and processor with EDF criteria
        soft_job = None
        if ready_servers:
            # Select the job with the least server-deadline
            server = min(ready_servers, key=lambda x: x.current_deadline)
            soft_job = server.ready_list[0]

        # COMPARISON
        job = soft_job
        type = "Soft"

        if soft_job is None:
            type = "Hard"
            job = hard_job

        if not soft_job is None and not hard_job is None and hard_job.absolute_deadline < self.cbs_servers[
            job.task].current_deadline:
            type = "Hard"
            job = hard_job

        if job is not None and job != cpu_min.running:
            if (cpu_min.running is None):
                if type == "Hard":
                    return self.execute_hard(job, cpu_min)
                res = self.execute_soft(job, cpu_min)
                return res

            if type == "Hard":
                if (self.is_soft_job(cpu_min.running) and
                        self.cbs_servers[cpu_min.running.task].current_deadline > job.absolute_deadline):
                    return self.execute_hard(job, cpu_min)
                elif (cpu_min.running.absolute_deadline > job.absolute_deadline):
                    return self.execute_hard(job, cpu_min)
            else:
                if (self.is_soft_job(cpu_min.running) and
                        self.cbs_servers[cpu_min.running.task].current_deadline > self.cbs_servers[
                            job.task].current_deadline):
                    return self.execute_soft(job, cpu_min)
                elif (cpu_min.running.absolute_deadline > self.cbs_servers[job.task].current_deadline):
                    return self.execute_soft(job, cpu_min)

    def execute_hard(self, job, cpu):
        print(self.sim.now(), job.name, cpu.name)

        # stop runtime timer for the job-server running on the selected processor
        if (cpu.running and self.is_soft_job(cpu.running)):
            self.cbs_servers[cpu.running.task].timer_runtime.stop()

        return (job, cpu)

    def execute_soft(self, job, cpu):
        # start runtime timer of the new server selected
        self.cbs_servers[job.task].timer_runtime = Timer(self.sim, EDF_CBS.runtime_call,
                                                         (self, self.cbs_servers[job.task]),
                                                         self.cbs_servers[job.task].current_runtime, one_shot=True,
                                                         cpu=self.processors[0], overhead=.000)
        self.cbs_servers[job.task].timer_runtime.start()
        self.cbs_servers[job.task].last_update = self.sim.now_ms()
        return self.execute_hard(job, cpu)

    def deadline_call(self, server):
        # This call is done when a CBS deadline expired
        # The runtime is refilled, a new deadline-server is computed and
        # the deadline-time is restarted
        if server.ready_list:
            server.set(server.maximum_runtime,
                       self.sim.now_ms() + server.period,
                       self.sim.now_ms(),
                       Timer(self.sim, EDF_CBS.deadline_call,
                             (self, server), server.deadline, one_shot=True,
                             cpu=self.processors[0], overhead=.000))
        server.task.cpu.resched()

    def runtime_call(self, server):
        # This call is done when the CBS runtime is consummed by a job-server
        # The state of the server becomes Throttled and the job is preempted
        server.is_throttled = True
        server.task.cpu.preempt()
        server.task.cpu.resched()


class CBSServer():
    def __init__(self, task, cbs_period, cbs_maximum_runtime, cbs_deadline):
        self.task = task
        self.period = cbs_period
        self.maximum_runtime = cbs_maximum_runtime
        self.deadline = cbs_deadline
        self.current_deadline = 0.
        self.current_runtime = 0.
        self.last_update = 0.
        self.ready_list = []
        self.is_throttled = False
        self.timer_runtime = None
        self.timer_deadline = None

    def __str__(self):
        st = ""
        st = "Server %s (%s,%s,%s) " % (self.task.name, self.maximum_runtime, self.period, self.deadline)
        st += " d:" + str(self.current_deadline) + " q:" + str(self.current_runtime)
        return st

    def add_job(self, job):
        self.ready_list.append(job)

    def remove_job(self, job):
        self.ready_list.remove(job)
        if (not self.ready_list):
            self.current_deadline = 0.
            self.current_runtime = 0.
            self.timer_deadline.stop()
            if self.timer_runtime:
                self.timer_runtime.stop()

    def set(self, q, d, time, timer_deadline):
        self.current_runtime = q
        self.current_deadline = d
        self.timer_deadline = timer_deadline
        self.timer_deadline.start()
        self.last_update = time
        self.is_throttled = False

    def update_runtime(self, time):
        self.current_runtime = self.current_runtime - (time - self.last_update)
        self.last_update = time
