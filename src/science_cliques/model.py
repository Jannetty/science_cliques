import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from science_cliques.individual import Individual


def get_agents_personal_rewire(skeptical: bool, reid: bool) -> int:
    if skeptical == True or reid == True:
        return 0
    return 1


def calculate_default_reliability() -> float:
    alpha = 1.5
    beta = 1
    reliability = np.random.beta(a=alpha, b=beta)
    return reliability


class CliqueModel(Model):
    """Model of emergent behavior of communities given testimonial norms

    ...

    Construction Parameters:
        number_of_individuals : int
            number of individuals in the model

        number_of_neighbors : int
            number of neighbors each individual will solicit for info
            floor of number_of_individuals * neighbor_percent

        num_facts : int
            number of overall facts that can be learned

        starting_knowledge : int
            number of facts agents begin having a belief about

        skeptical : bool
            if true, agents take skeptical philosophy, only believe facts they
            discover through observation (never believe neighbors. False if reid,
            direct, or indirect are true.

        reid : bool
            if true, agents take on crudalist philosophy (initially interact
            with random neighbors and never change. False if skeptical, direct or
            indirect are true.

        direct : bool
            if true, agents take on objective reductionist philosophy (connect
            with agents who have the highest % of true beliefs). False if
            skeptical reid or indirect are true

        indirect : bool
            if true, agents take on subjective reductionist philosophy (connect
            with agents who have the highest % agreement with themselves). False
            if skeptical, reid or direct are true.

    ...
    Attributes
        truth_mean : float
            all agent's true beliefs / (all agents's true beliefs + all agent's
            false beliefs)

        total_truth : int
            sum of all agent's true beliefs

        agreement_stats : list of lists
            number_of_individuals by number_of_individuals matrix that contains
            degree of agreement between two agents. Symmetric matrix

        reliability_stats : list
            number_of_individuals length list that holds truth_mean of each
            individual (index of list = id of individual with that truth_mean)


    """

    def check_params(
        self,
        number_of_individuals: int,
        number_of_neighbors: int,
        num_facts: int,
        starting_knowledge: int,
        skeptical: bool,
        reid: bool,
        direct: bool,
        indirect: bool,
    ) -> None:
        if (skeptical + reid + direct + indirect) == 0:
            raise ValueError(
                "Please set one (and only one) of the following "
                "to True: skeptical, reid, direct, or indirect"
            )
        if (skeptical + reid + direct + indirect) > 1:
            raise ValueError(
                "Only one of [skeptical, reid, direct, indirect] "
                "can be set to True. Please set one to True and "
                "all others to False."
            )
        if starting_knowledge >= num_facts:
            raise ValueError("starting_knowledge must be lower than num_facts")
        if num_facts <= 0:
            raise ValueError("num_facts must be greater than 0")

    def make_agreement_stats_matrix(self, number_of_individuals: int) -> list:
        agreement_stats = []
        for individual_row in range(number_of_individuals):
            row = []
            for individual_col in range(number_of_individuals):
                col = []
                row.append(col)
            agreement_stats.append(row)
        return agreement_stats

    def set_philosophy(self, skeptical: bool, reid: bool, direct: bool, indirect: bool) -> None:
        if skeptical:
            self.philosophy = "skeptical"
        elif reid:
            self.philosophy = "reid"
        elif direct:
            self.philosophy = "direct"
        elif indirect:
            self.philosophy = "indirect"

    def __init__(
        self,
        number_of_individuals: int = 100,
        number_of_neighbors: int = 6,
        num_facts: int = 1500,
        starting_knowledge: int = 15,
        skeptical: bool = False,
        reid: bool = False,
        direct: bool = False,
        indirect: bool = False,
    ) -> None:

        # make sure parameters passed are valid
        self.check_params(
            number_of_individuals,
            number_of_neighbors,
            num_facts,
            starting_knowledge,
            skeptical,
            reid,
            direct,
            indirect,
        )

        # run super initalizing function
        super().__init__()

        # set constructor attributes
        self.num_agents = number_of_individuals
        self.num_neighbors = number_of_neighbors
        self.num_facts = num_facts
        self.set_philosophy(skeptical, reid, direct, indirect)

        # set other attributes
        self.schedule = RandomActivation(self)
        self.truth_mean = 0.0
        self.total_truth = 0
        self.agreement_stats = self.make_agreement_stats_matrix(number_of_individuals)
        self.reliability_stats = [None] * self.num_agents

        # determine agents' personal_rewire value
        agent_personal_rewire = get_agents_personal_rewire(skeptical, reid)

        # create agents
        for i in range(self.num_agents):
            # calculate reliability
            reliability = calculate_default_reliability()
            new_individual = Individual(
                unique_id=i,
                model=self,
                personal_rewire=agent_personal_rewire,
                starting_knowledge=starting_knowledge,
                reliability=reliability,
                philosophy=self.philosophy,
            )
            # add to reliability_stats list
            self.reliability_stats[i] = new_individual.truth_mean
            print(new_individual.truth_mean)
            self.schedule.add(new_individual)

    def update_reliability_stats(self) -> None:
        """ Iterates through all individuals in model and sets
        reliability_stats[agent_id] to that agent's truth_mean"""
        for key_id in self.schedule._agents:
            self.reliability_stats[key_id] = self.schedule._agents[
                key_id].truth_mean


    def step(self) -> None:
        """Advance the model by one step."""
        self.schedule.step()
        self.update_reliability_stats()
