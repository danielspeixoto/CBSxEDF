import sys
from simso.core import Model, Results, ProcEvent, Results
from simso.configuration import Configuration
from simso.core import Task
from simso.generator import task_generator
from scheduling import run

# parameters
num_tasks = [100]
utilization = [20]
num_sets = 1
soft_contrib = [0.9]
percents = [0.6]
duration = 1000

def init_dict_tasks(dict, type):
    dict[type + '_abort_count'] = 0
    dict[type + '_preemption_count'] = 0

def entry(dict, type, task):
    dict[type + '_abort_count'] += task.abort_count
    for job in task.jobs:
        dict[type + '_preemption_count'] += job.preemption_count

def analysis(result):
    # abort_count
    dict = {}
    dict['total_migrations'] = result.total_migrations
    dict['total_preemptions'] = result.total_preemptions
    dict['total_task_migrations'] = result.total_task_migrations
    dict['total_task_resumptions'] = result.total_task_resumptions
    dict['total_exceeded_count'] = result.total_exceeded_count
    init_dict_tasks(dict, 'soft')
    init_dict_tasks(dict, 'hard')
    for key, value in result.tasks.iteritems():
        if value.task.data['soft']:
            entry(dict, 'soft', value)
        else:
            entry(dict, 'hard', value)

    for key, value in result.processors.iteritems():
        dict['proc_save_count'] = value.context_save_count
        dict['proc_save_overhead'] = value.context_save_overhead
        dict['proc_load_count'] = value.context_load_count
        dict['proc_load_overhead'] = value.context_load_overhead

    return dict


for tasks in num_tasks:
    for soft in soft_contrib:
        for util in utilization:
            for dev in percents:
                cbs, edf = run(num_sets, tasks, util, dev, soft, duration)
                print("CBS")
                cbs_data = analysis(cbs)
                print(cbs_data)
                print("EDF")
                edf_Data = analysis(edf)
                print(edf_Data)


