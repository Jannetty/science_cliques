import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from science_cliques.individual import Individual


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

        investigation_probability : float
            probability agents will observe something about the world on a run

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

        false_mean : float
            all agents/ false beliefs / (all agents' beliefs)

        total_false : int
            sum of all agent's false beliefs

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
                col = [None]
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
        investigation_probability: float = 0.1,
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
        self.starting_knowledge = starting_knowledge

        # set other attributes
        self.schedule = RandomActivation(self)
        self.truth_mean = 0.0
        self.false_mean = 0.0
        self.total_truth = 0
        self.total_false = 0
        self.reliability_stats = [None] * self.num_agents

        # create agents
        for i in range(self.num_agents):
            # calculate reliability
            reliability = calculate_default_reliability()
            new_individual = Individual(
                unique_id=i,
                model=self,
                starting_knowledge=starting_knowledge,
                reliability=reliability,
                philosophy=self.philosophy,
                investigation_probability=investigation_probability,
            )
            # add to reliability_stats list (updates reliability_stats)
            self.reliability_stats[i] = new_individual.truth_mean
            self.schedule.add(new_individual)

        # initialize and update agreement stats
        self.update_agreement_stats()

    def update_reliability_stats(self) -> None:
        """Iterates through all individuals in model and sets
        reliability_stats[agent_id] to that agent's truth_mean"""
        for key_id in self.schedule._agents:
            self.reliability_stats[key_id] = self.schedule._agents[key_id].truth_mean

    def update_agreement_stats(self) -> None:
        """Iterates through all individuals and calculates percent
        agreement, saves values in agreement_stats"""
        new_agreement_stats = self.make_agreement_stats_matrix(self.num_agents)
        # for every pair of agents calculate agreement
        for key_id1 in self.schedule._agents:
            for key_id2 in self.schedule._agents:
                # set all selves to be -1
                if key_id1 == key_id2:
                    new_agreement_stats[key_id1][key_id2] = -1
                    new_agreement_stats[key_id2][key_id1] = -1
                if key_id1 != key_id2 and new_agreement_stats[key_id1][key_id2] == [None]:
                    agreement = self.schedule._agents[key_id1].calculate_agreement(
                        self.schedule._agents[key_id2]
                    )
                    new_agreement_stats[key_id1][key_id2] = agreement
                    # make symmetrical
                    new_agreement_stats[key_id2][key_id1] = agreement
        self.agreement_stats = new_agreement_stats

    def update_model_truth_false_mean_and_truth_false_total(self):
        """Updates model's count of the percent of beliefs in the model that
        are true and the total number of beliefs in the model that are true
        (and complimentary false statistics)"""
        truth_means = []
        truth_totals = []
        false_means = []
        false_totals = []
        for key_id in self.schedule._agents:
            this_truth_mean = self.schedule._agents[key_id].truth_mean
            truth_means.append(this_truth_mean)
            this_truth_total = self.schedule._agents[key_id].truth_total
            truth_totals.append(this_truth_total)
            this_false_mean = self.schedule._agents[key_id].false_mean
            false_means.append(this_false_mean)
            this_false_total = self.schedule._agents[key_id].false_total
            false_totals.append(this_false_total)

        truth_mean = sum(truth_means) / len(truth_means)
        truth_total = sum(truth_totals)
        false_mean = sum(false_means) / len(false_means)
        false_total = sum(false_totals)

        self.truth_mean = truth_mean
        self.total_truth = truth_total
        self.false_mean = false_mean
        self.total_false = false_total

    def step(self) -> None:
        """Advance the model by one step."""
        self.schedule.step()
        self.update_reliability_stats()
        self.update_agreement_stats()
