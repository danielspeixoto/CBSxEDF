import errno
import os
import pickle
import sys
from simso.core import Model, Results, ProcEvent, Results
from simso.configuration import Configuration
from simso.core import Task
from simso.generator import task_generator
from scheduling import run
import constants
import timeit


def create_file(path, name, obj):
    file_pth = path + "/" + name
    if not os.path.exists(os.path.dirname(file_pth)):
        try:
            os.makedirs(os.path.dirname(file_pth))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(file_pth , 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


start_time = timeit.default_timer()
for tasks in constants.num_tasks:
    for cpu in constants.cpu_count:
        for soft in constants.soft_contrib:
            for util in constants.utilization:
                util *= cpu
                cbs, edf = run(constants.num_sets, tasks, util, constants.percents, soft, constants.duration, cpu)
                path = 'results_wcetXacet/' + str(tasks) + "/" + str(cpu) + "/" + str(soft) + "/" + str(util)

                create_file(path, "cbs.pkl", cbs)
                create_file(path, "edf.pkl", edf)

elapsed = timeit.default_timer() - start_time
minutes = elapsed / 60
print("Took " + str(minutes) + " minutes to finish")