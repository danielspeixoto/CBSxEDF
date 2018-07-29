# This Python file uses the following encoding: utf-8

import pickle
import matplotlib
import constants
import matplotlib.pyplot as plt


def get_type(pos):
    if pos == 0:
        return constants.num_tasks
    if pos == 1:
        return constants.cpu_count

    if pos == 2:
        return constants.soft_contrib

    if pos == 3:
        return constants.utilization


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def get_instance(tasks, cpu, soft, util):
    return 'results_wcetXacet/' + str(tasks) + "/" + str(cpu) + "/" + str(soft) + "/" + str(util)


def get_range(view):
    ranges = []
    if view[0] == None:
        idx = len(constants.num_tasks)
        ranges.append((0, idx))
    else:
        idx = constants.num_tasks.index(view[0])
        ranges.append((idx, idx + 1))
    if view[1] == None:
        idx = len(constants.cpu_count)
        ranges.append((0, idx))
    else:
        idx = constants.cpu_count.index(view[1])
        ranges.append((idx, idx + 1))
    if view[2] == None:
        idx = len(constants.soft_contrib)
        ranges.append((0, idx))
    else:
        idx = constants.soft_contrib.index(view[2])
        ranges.append((idx, idx + 1))
    if view[3] == None:
        idx = len(constants.utilization)
        ranges.append((0, idx))
    else:
        idx = constants.utilization.index(view[3])
        ranges.append((idx, idx + 1))
    return ranges

def get_name(view):
    if view[0] == None:
        return unicode('Número de Tasks', 'utf-8')
    if view[1] == None:
        return unicode('Número de Processadores', 'utf-8')
    if view[2] == None:
        return unicode('Porcentagem de Soft Tasks', 'utf-8')
    if view[3] == None:
        return unicode('Utilização', 'utf-8')

# tasks #cpus #porc #util
views = [[50, 1, None,  5]]
methods = ['cbs', 'edf']
params = [
            'total_preemptions',
            'total_task_migrations',
            'hard_abort_count',
            'soft_abort_count',
            'hard_preemption_count',
            'soft_preemption_count'
        ]
param_pt = {
    'total_preemptions': unicode('Prempções', 'utf-8'),
    'total_task_migrations': unicode('Migrações', 'utf-8'),
    'hard_abort_count': unicode('Quantidade de vezes que uma Hard Task é abortada', 'utf-8'),
    'soft_abort_count': unicode('Quantidade de vezes que uma Soft Task é abortada', 'utf-8'),
    'hard_preemption_count': unicode('Quantidade de vezes que uma Hard Task é preemptada', 'utf-8'),
    'soft_preemption_count': unicode('Quantidade de vezes que uma Soft Task é preemptada', 'utf-8')
}
for view in views:
    idxs = get_range(view)
    dict = {}
    for method in methods:
        dict[method] = {}
        for param in params:
            dict[method][param] = []
        for tasks_idx in range(idxs[0][0], idxs[0][1]):
            task = constants.num_tasks[tasks_idx]
            for cpu_idx in range(idxs[1][0], idxs[1][1]):
                cpu = constants.cpu_count[cpu_idx]
                for soft_idx in range(idxs[2][0], idxs[2][1]):
                    soft = constants.soft_contrib[soft_idx]
                    for util_idx in range(idxs[3][0], idxs[3][1]):
                        util = constants.utilization[util_idx]
                        path = get_instance(task, cpu, soft, util * cpu)
                        print("Instance Params: " +
                              " tasks " + str(task) +
                              " cpu " + str(cpu) +
                              " soft " + str(soft) +
                              " util " + str(util  * cpu))
                        obj = load_obj(path + "/" + method)
                        for param in params:
                            dict[method][param].append(obj[param])
                        dict[method]['hard_abort_count'][len(dict[method]['hard_abort_count']) - 1] /= (task * (1 - soft))
                        dict[method]['soft_abort_count'][len(dict[method]['soft_abort_count']) - 1] /= (task * soft)
                        dict[method]['hard_preemption_count'][len(dict[method]['hard_preemption_count']) - 1] /= (
                                    task * (1 - soft))
                        dict[method]['soft_preemption_count'][len(dict[method]['soft_preemption_count']) - 1] /= (task * soft)
                        # print("EDF")
                        # print(load_obj(path + "/edf"))
    type = get_type(view.index(None))

    # for method in methods:
    #     for i in range(len(dict[method]['hard_abort_count'])):
    #         dict[method]['hard_abort_count'][i] /=
    # for item in

    for param in params:
        plt.figure()
        for method in methods:
            plt.plot(type, dict[method][param])
        plt.title(param_pt[param])
        plt.xlabel(get_name(view))
        plt.legend(methods)
    plt.show()

