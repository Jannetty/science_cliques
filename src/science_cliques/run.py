# from mesa import Agent, Model
from model import CliqueModel

# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    model = CliqueModel(15, direct=True)
    model.step()
