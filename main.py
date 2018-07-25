import sys
from simso.core import Model, Results, ProcEvent, Results
from simso.configuration import Configuration
from simso.core import Task
from simso.generator import task_generator

# Manual configuration:
configuration = Configuration()

# Amount of ms for the experiment
configuration.duration = 200 * configuration.cycles_per_ms

# Add tasks:
num_tasks = 2
utilization = 0.8
num_sets = 1
# n and u are incorrectly placed
ut = task_generator.gen_uunifastdiscard(nsets=num_sets, u=num_tasks, n=utilization)
pd = task_generator.gen_periods_uniform(num_tasks, num_sets, 1, 5)
print(ut)
print(pd)

tset = task_generator.gen_tasksets(ut, pd)
print(tset)

# print(task_generator.gen_ripoll(num_sets, 1, 3, 0, 1))
#
# # Add a processor:
# configuration.add_processor(name="CPU 1", identifier=1)
#
# # Add a scheduler:
# #configuration.scheduler_info.filename = "examples/RM.py"
# configuration.scheduler_info.clas = "simso.schedulers.EDF"
#
# # Check the config before trying to run it.
# configuration.check_all()
#
# # Init a model from the configuration.
# model = Model(configuration)
#
# # Execute the simulation.
# model.run_model()
#
# # Print logs.
# for log in model.logs:
#     print(log)
#
# cxt = 0
# for processor in model.processors:
#     prev = None
#     for evt in processor.monitor:
#         if evt[1].event == ProcEvent.RUN:
#             if prev is not None and prev != evt[1].args.task:
#                 cxt += 1
#             prev = evt[1].args.task
#
# print("Number of context switches (without counting the OS): " + str(cxt))
#
# print(model.results.scheduler.activate_count)