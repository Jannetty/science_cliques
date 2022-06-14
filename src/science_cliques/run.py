# from mesa import Agent, Model
from science_cliques.model import CliqueModel

# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    model = CliqueModel(direct=True, number_of_individuals=8)
    model.step()
