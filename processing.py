import pickle

import constants


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


for tasks in constants.num_tasks:
    for cpu in constants.cpu_count:
        for soft in constants.soft_contrib:
            for util in constants.utilization:
                path = 'results/' + str(tasks) + "/" + str(cpu) + "/" + str(soft) + "/" + str(util)
                print(load_obj(path + "/cbs"))