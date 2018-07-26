import sys
from simso.core import Model, Results, ProcEvent, Results
from simso.configuration import Configuration
from simso.core import Task
from simso.generator import task_generator

# Manual configuration:
configuration = Configuration()
configuration.etm = 'acet'

# Amount of ms for the experiment
configuration.duration = 20 * configuration.cycles_per_ms

# Add tasks:
num_tasks = 2
utilization = 0.8
num_sets = 1
# n and u are incorrectly placed
ut = task_generator.gen_uunifastdiscard(nsets=num_sets, u=num_tasks, n=utilization)
pd = task_generator.gen_periods_uniform(num_tasks, num_sets, 2, 10)
tset = task_generator.gen_tasksets(ut, pd)
# print("Utilization")
# print(ut)
# print("Periods")
# print(pd)
# print("Task Set")
# print(tset)

tset = [[(1.649366, 6.088448), (4.304636, 8.135785)]]

counter = 0
for set in tset:
    for task in set:
        configuration.add_task(name="Task" + str(counter),
                               identifier=counter,
                               period=task[1],
                               deadline=task[1],
                               # wcet=task[0],
                               acet=task[0]
                               )
        counter += 1


# configuration.add_task(name="T1", identifier=1, period=7,
#                        activation_date=0, wcet=3, deadline=7)
# configuration.add_task(name="T2", identifier=2, period=12,
#                        activation_date=0, wcet=3, deadline=12)
# configuration.add_task(name="T3", identifier=3, period=20,
#                        activation_date=0, wcet=5, deadline=20)
# print(task_generator.gen_ripoll(num_sets, compute=100, deadline=1000, period=0, target_util=0.85))

# Add a processor:
configuration.add_processor(name="CPU 1", identifier=1)

# Add a scheduler:
#configuration.scheduler_info.filename = "examples/RM.py"
configuration.scheduler_info.clas = "simso.schedulers.EDF"

# Check the config before trying to run it.
configuration.check_all()

# Init a model from the configuration.
model = Model(configuration)

# Execute the simulation.
model.run_model()

# Print logs.
print("Logs")
for log in model.logs:
    print(log)

cxt = 0
for processor in model.processors:
    prev = None
    for evt in processor.monitor:
        if evt[1].event == ProcEvent.RUN:
            if prev is not None and prev != evt[1].args.task:
                cxt += 1
            prev = evt[1].args.task

# print("Number of context switches (without counting the OS): " + str(cxt))
#
# print(model.results.scheduler.activate_count)