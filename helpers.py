# configuration.add_task(name="Task " + str(counter) + " Hard",
#                        identifier=1,
#                        period=3,
#                        deadline=3,
#                        # WCET is not know
#                        wcet=2,
#                        acet=2,
#                        data={
#                            'cbs_period': 3,
#                            'cbs_maximum_runtime': 2,
#                            'cbs_deadline': 3
#                        }
#                        )
#
#
# configuration.add_task(name="Task " + str(counter) + " Soft",
#                        identifier=2,
#                        task_type='Periodic',
#                        abort_on_miss=False,
#                        period=7,
#                        deadline=7,
#                        # TODO Normal distribution to find out
#                        wcet=2,
#                        acet=2,
#                        et_stddev=std_dev,
#                        data={
#                            'soft': True,
#                            'cbs_period': 7,
#                            'cbs_maximum_runtime': 2,
#                            'cbs_deadline': 7
#                        }
#                        )