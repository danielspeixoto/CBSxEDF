
from simso.core import Model
from simso.configuration import Configuration
from simso.generator import task_generator
from tasks import create, add
import analysis

DEBUG = True


def default_config(duration, cpu_count):
    config = Configuration()

    # Amount of ms for the experiment
    config.cycles_per_ms = 100000
    config.duration = duration * config.cycles_per_ms

    # Add a processor:
    for i in range(cpu_count):
        config.add_processor(name="CPU " + str(i), identifier=i)
    return config


def config_cbs(config):
    config.scheduler_info.filename = "./EDF_CBS.py"
    config.etm = 'acet'


def config_edf(config):
    config.scheduler_info.clas = 'simso.schedulers.EDF'
    config.etm = 'acet'


def run(num_sets, num_tasks, utilization, percent, soft_contrib, duration, cpu_count):
    # Create taskset
    tset = create(num_sets, num_tasks, utilization)
    cbs_res = None
    edf_res = None
    for tasks in tset:
        config = default_config(duration, cpu_count)
        add(config, tasks, percent, soft_contrib)

        config_cbs(config)
        cbs_res = analysis.merge(analysis.analysis(run_model(config)), cbs_res)

        config_edf(config)
        edf_res = analysis.merge(analysis.analysis(run_model(config)), edf_res)


    return analysis.division(cbs_res, len(tset)), analysis.division(edf_res, len(tset))


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
