from multiprocessing import Pool
from backend.models.seihrd_model import run_seihrd


def execute(params):

    return run_seihrd(**params)


def parallel_simulations(
    scenarios
):

    with Pool(4) as pool:

        results = pool.map(
            execute,
            scenarios
        )

    return results