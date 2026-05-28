from backend.models.sir_model import run_sir
from backend.models.seir_model import run_seir
from backend.models.seihrd_model import run_seihrd


def simulate(data):

    model = data["model"]

    if model == "SIR":

        return run_sir(
            population=data["population"],
            infected=data["infected"],
            recovered=0,
            beta=data["beta"],
            gamma=data["gamma"],
            days=data["days"]
        )

    elif model == "SEIR":

        return run_seir(
            population=data["population"],
            exposed=data["exposed"],
            infected=data["infected"],
            recovered=0,
            beta=data["beta"],
            sigma=data["sigma"],
            gamma=data["gamma"],
            days=data["days"]
        )

    elif model == "SEIHRD":

        return run_seihrd(**data)