from mesa import Model
from mesa.time import RandomActivation
from individual import Individual


class CliqueModel(Model):
    """A model with some number of agents."""

    def __init__(self, N: int):
        super().__init__()
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            new_individual = Individual(i, self)
            self.schedule.add(new_individual)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
