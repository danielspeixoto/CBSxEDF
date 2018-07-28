from simso.core import Scheduler


class CBS(Scheduler):
    # TODO Define MAX_BUDGET anD PERIOD
    def __init__(self, max_b, p):
        self.ready_list = []
        # Max Budget
        self.max_budget = max_b
        # Current Budget
        self.current_budget = self.max_budget
        # Period
        self.period = p
        # Fixed Deadline
        self.deadline = 0
        self.num_pending_requests = 0
        self.release_time = 0
        self.iteration = 0

    def on_activate(self, job):
        self.ready_list.append(job)
        self.num_pending_requests = self.num_pending_requests + 1
        if self.num_pending_requests == 1: # idle
            # float?
            if job.activation_date + ( float(self.current_budget) / self.max_budget) * self.period >= self.deadline:
                self.iteration = self.iteration + 1
                self.release_time = job.activation_date
                self.deadline = self.release_time + self.period
                self.current_budget = self.max_budget
            else:
                self.iteration = self.iteration + 1
                self.release_time = job.activation_date
                # self.d = self.dA

        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        self.num_pending_requests = self.num_pending_requests - 1

        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:  # If at least one job is ready:
            job = self.ready_list[0]
            # Check if method is correct
            # Check if this returns all comp time or only executed time
            # Job served by S executes for a time unit
            self.current_budget = self.current_budget - job.computation_time
            if self.current_budget < 0:
                print("Error: C < 0")
            if self.current_budget == 0:
                self.iteration = self.iteration + 1
                self.release_time = self.sim.now()
                self.deadline = self.deadline + self.period
                self.current_budget = self.max_budget

        else:
            job = None
        return(job, cpu)