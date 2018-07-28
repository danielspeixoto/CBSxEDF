
from simso.core import Model
from simso.configuration import Configuration
from simso.generator import task_generator
from tasks import create, add

DEBUG = True


def default_config(duration):
    config = Configuration()

    # Amount of ms for the experiment
    config.cycles_per_ms = 100000
    config.duration = duration * config.cycles_per_ms

    # Add a processor:
    config.add_processor(name="CPU 1", identifier=1)
    return config


def config_cbs(config):
    config.scheduler_info.filename = "./EDF_CBS.py"
    config.etm = 'acet'


def config_edf(config):
    config.scheduler_info.clas = 'simso.schedulers.EDF'
    config.etm = 'acet'


def run(num_sets, num_tasks, utilization, percent, soft_contrib, duration):
    # Create taskset
    tset = create(num_sets, num_tasks, utilization)
    for tasks in tset:
        config = default_config(duration)
        add(config, tasks, percent, soft_contrib)

        config_cbs(config)
        cbs_results = run_model(config)

        config_edf(config)
        edf_results = run_model(config)

        return cbs_results, edf_results


def run_model(config):
    model = Model(config)

    # Execute the simulation.
    model.run_model()

    # Print logs.
    if DEBUG:
        print("Logs ")
        for log in model.logs:
            print(log)

    return model.results
