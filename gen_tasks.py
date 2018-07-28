from simso.generator import task_generator


def get_tasks(num_tasks, utilization, num_sets=1):
    num_tasks = 2
    utilization = 0.5
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
    # print(" ")

    # counter = 0
    # for set in tset:
    #     for task in set:
    #         configuration.add_task(name="Task" + str(counter),
    #                                identifier=counter,
    #                                period=task[1],
    #                                deadline=task[1],
    #                                # WCET is not know
    #                                wcet=float("inf"),
    #                                acet=task[0],
    #                                # TODO How to calculate that
    #                                et_stddev=0
    #                                )
    #         counter += 1

    configuration.add_task(name="TaskHard",
                                   identifier=1,
                                   period=3,
                                   deadline=3,
                                   # WCET is not know
                                   wcet=2,
                                   acet=2
                                   )

    configuration.add_task(name="TaskSoft",
                                   identifier=2,
                                    task_type='Sporadic',
                           abort_on_miss=False,
                                    list_activation_dates=[2,5,8,11,14,17],
                                   period=3,
                                   deadline=3,
                                   # WCET is not know
                                   wcet=float("inf"),
                                   acet=1
                                   )

    # print(task_generator.gen_ripoll(num_sets, compute=100, deadline=1000, period=0, target_util=0.85))