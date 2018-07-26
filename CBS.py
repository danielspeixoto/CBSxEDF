from simso.core import Scheduler


class CBS(Scheduler):
    def init(self):
        self.ready_list = []
        # Max Budget
        self.Q = 10
        # Current Budget
        self.c = self.Q
        # Period
        self.T = 10
        # Fixed Deadline
        self.d = 0
        self.n = 0
        self.k = 0
        self.a = 0

    def setQ(self, q):
        self.Q = q
        self.c = self.Q

    def on_activate(self, job):
        self.ready_list.append(job)
        self.n = self.n + 1
        if self.n == 1:
            # float?
            if 11 + (self.c / self.Q) * self.T >= self.d:
                self.k = self.k + 1
                self.a = job.activation_date()
                self.d = self.a + self.T
                self.c = self.Q
            else:
                self.k = self.k + 1
                self.a = job.activation_date()
                self.d = self.d

        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        self.n = self.n - 1
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:  # If at least one job is ready:
            job = self.ready_list[0]



            # Check if method is correct
            # Check if this returns all comp time or only executed time
            # Job served by S executes for a time unit
            self.c = self.c - job.computation_time()
            if self.c < 0:
                print("Error: C < 0")
            if self.c == 0:
                self.k = self.k + 1
                self.a = self.sim.now()
                self.d = self.d + self.T
                self.c = self.Q

        else:
            job = None
        pass