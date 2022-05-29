from mesa import Agent
from model import Model


class Individual(Agent):
    """An agent."""

    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.starting_knowledge = 10

    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        print("Hi, I am agent " + str(self.unique_id) + ".")
