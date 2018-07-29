from simso.generator import task_generator


def create(num_sets, num_tasks, utilization):
    ut = task_generator.gen_randfixedsum(num_sets, num_tasks, utilization)
    ut2 = ut
    pd = task_generator.gen_periods_uniform(num_tasks, num_sets, 2, 100)
    tset = task_generator.gen_tasksets(ut2, pd)

    # print(tset)
    # tset_wcet = []
    # for set in tset:
    #     tset_wcet.append([])
    #     for task in set:
    #         tset_wcet[len(tset_wcet) - 1].append((
    #             task[0], # Acet
    #             task[1], # Period
    #             get_acet_from_wcet(task[0], task[0]/10) # Wcet
    #         ))
    #     print(tset_wcet[len(tset_wcet) - 1])

    return tset


def add(config, tasks, percent, soft_contrib):
    num_tasks = len(tasks)

    soft_tasks_amount = int(num_tasks * soft_contrib)
    hard_tasks_amount = num_tasks - soft_tasks_amount

    counter = 0
    for task in tasks:
        if hard_tasks_amount > 0:
            config.add_task(name="Task " + str(counter) + " Hard",
                            identifier=counter,
                            period=task[1],
                            deadline=task[1],
                            wcet=task[0],
                            acet=task[0],
                            # Ebforces that wcet is used
                            et_stddev=0,
                            data={
                                'soft': False,
                                'cbs_period': task[1],
                                'cbs_maximum_runtime': task[0],
                                'cbs_deadline': task[1]
                            }
                            )
            hard_tasks_amount -= 1
        else:
            config.add_task(name="Task " + str(counter) + " Soft",
                            identifier=counter,
                            # TODO Check if it is aborted
                            # abort_on_miss=False,
                            period=task[1],
                            deadline=task[1],
                            wcet=task[0],
                            acet=get_acet_from_wcet(task[0], percent),
                            et_stddev=task[0] * percent,
                            data={
                                'soft': True,
                                'cbs_period': task[1],
                                'cbs_maximum_runtime': get_acet_from_wcet(task[0], percent),
                                'cbs_deadline': task[1]
                            }
                            )

        counter += 1

z = 1.5
def get_wcet_from_acet(acet, std_dev):
    return z * std_dev + acet

def get_acet_from_wcet(wcet, percent):
    # res = 0
    # counter = 0
    # while(res <= 0):
    #     res = wcet - (z - 0.1 * counter) * std_dev
    #     counter += 1
    # return res
    return wcet - z * (wcet * percent)