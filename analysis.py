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


def merge(dict1, dict2):
    if dict2 is not None:
        dict = {}
        for item in dict1.iteritems():
            dict[item[0]] = dict1[item[0]] + dict2[item[0]]
        return dict
    return dict1

def division(dict, div):
    for item in dict.iteritems():
        dict[item[0]] = item[1]/div
    return dict
