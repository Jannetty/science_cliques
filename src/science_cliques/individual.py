import numpy as np
import random

from mesa import Agent
from mesa import Model


def get_ties(aList: list, element) -> list:
    """Takes a list and a list element, returns all indices that contain that
    element"""
    tie_idxs = [i for i, j in enumerate(aList) if j == element]
    return tie_idxs

def check_get_max_n_indices_params(value_list: list, n: int) -> None:
    """Checks to make sure list is list of floats, value_list > 1 element long,
    n > 1, and n <= len(value_list)"""
    for element in value_list:
        if not isinstance(element, float):
            raise (ValueError("value_list must be list of floats"))
    if len(value_list) < 1:
        raise ValueError("value_list must have at least one entry")
    if n < 1:
        raise ValueError("n must be at least 1")
    if n > len(value_list):
        raise ValueError("n must be less than or equal to len(value_list)")

def i_is_first_element(value_list: list, i: int) -> bool:
    """ Returns true if index i holds the last element of the list"""
    if i == 0:
        return True
    return False

def get_max_n_indices(value_list: list, n: int) -> list:
    """Returns the n indices of int list value_list that hold the maximum n
    values. If there are any ties in those top values, chooses between agents
    within tie randomly"""

    check_get_max_n_indices_params(value_list, n)

    # sort indices in descending order
    sorted_indices = np.argsort(value_list)

    max_indices = []
    i = len(sorted_indices) - 1
    # start at max element
    while len(max_indices) < n:
        potential_max = value_list[sorted_indices[i]]
        # if this is first element of list or the list doesn't have ties for
        # this
        # element, add it
        if i_is_first_element(value_list, i) or get_ties(value_list,
                                                        potential_max) == [i]:
            max_indices.append(sorted_indices[i])
            i = i - 1
        # otherwise find where all the ties are
        else:
            idx_of_matching_list_elements = get_ties(value_list, potential_max)
            # if all tied values can be added (n is big enough) add them all
            if len(max_indices) + len(idx_of_matching_list_elements) <= n:
                max_indices = max_indices + idx_of_matching_list_elements
                i = i - len(idx_of_matching_list_elements)

            # otherwise choose which ones are appended randomly
            else:
                # get number of tied elements to be added
                num_idx_to_choose = n - len(max_indices)
                # select that number of random indices from list of tied
                # element indicies
                random_idxs_of_matching_list_elements = \
                    random.sample(range(0,
                                        len(idx_of_matching_list_elements)),
                                   num_idx_to_choose)
                # append to list
                for idx in random_idxs_of_matching_list_elements:
                    max_indices.append(idx_of_matching_list_elements[idx])

    return max_indices



class Individual(Agent):
    """Individual Agent

    ...
    Constructor parameters
    ---
        unique_id : int
            unique agent identifier

        model : CliqueModel
            model the agent is a part of

        reliability : float
            likelihood that agent's personal_facts are true. By
            default, drawn from beta distribution with alpha = 1.5
            beta = 1 so that average over population is 60%

        starting_knowledge : int
            number of facts agents start off having a belief about (number of
            entries in personal_facts)

        philosophy : string
            'skeptical', 'reid', 'direct', or 'indirect'. Determines how
            agents form connections with other agents

        investigation_probability : float
            defaults to .1. Probability an agent observes something true about
            the world on each run.


    ...
    Attributes
    ---
        num_neighbors : int
            the number of agents each agent will ask for testimony

        unknown_personal_facts : int
            number of personal facts that have value 0

        unknown_social_facts : int
            number of social facts that have value 0

        unknown_total_facts : int
            number of facts that have value 0 in both personal_facts and
            social_facts

        truth_total : int
            total number of beliefs that have value 1

        false_total : int
            total number of beliefs that have value -1

        truth_mean : float
            (number of beliefs that have value == 1) / ((number of beliefs that
            have value == 1) + (number of beliefs that have values == -1))

        all_facts : list
            contains how agents feel about all facts

        personal_facts : list
            contains facts agent believes as result of direct observation.
            0 = abstain, 1 = true belief, -1 = false belief. Initialized to
            length(number_of_facts) list of all zeros except starting_knowledge
            number of beliefs. reliability percent of starting_knowledge beliefs
            will be true

        social_facts : list
            contains facts agent believes as result of social interaction.
            0 = abstain, 1 = true belief, -1 = false belief. Initialized to
            length(number_of_facts) list of all zeros

        index : array I think
            used in indirect_calibration_rewire to order agents who have highest
            agreement with this agent. I don't think we actually need this
            parameter but we'll see.

    ...

    Functions
    ---



    """

    def get_belief(self) -> int:
        """Determines whether an agent has a correct (1) or incorrect (-1)
        belief about a fact according to that agent's reliability"""
        random_fact_val = random.uniform(0, 1)
        if random_fact_val <= self.reliability:
            return 1
        elif random_fact_val > self.reliability:
            return -1

    def get_random_index_of_abstained_belief(self) -> int:
        """Selects a random belief about which this individual has no
        beliefs"""
        index = random.randint(0, self.num_facts - 1)
        # make sure this index doesn't currently hold a belief
        while self.all_facts[index] != 0:
            index = random.randint(0, self.num_facts - 1)
        return index

    def initialize_personal_facts(self, num_facts: int, starting_knowledge: int) -> None:
        """Makes personal_facts list and populates it with a
        starting_knowledge number of beliefs"""
        self.personal_facts = [0] * num_facts
        for i in range(starting_knowledge):
            index = self.get_random_index_of_abstained_belief()
            self.personal_facts[index] = self.get_belief()

    def update_all_facts(self):
        """ Collects all beliefs about all facts in one list"""
        all_facts = [0] * len(self.all_facts)
        for i in range(len(self.personal_facts)):
            if self.personal_facts[i] != 0:
                all_facts[i] = self.personal_facts[i]
            if self.social_facts[i] != 0:
                all_facts[i] = self.social_facts[i]
        self.all_facts = all_facts


    def __init__(
        self,
        unique_id: int,
        model: Model,
        starting_knowledge,
        reliability: float,
        philosophy: str,
        investigation_probability: float = 0.1,
    ) -> None:
        """Initializes a new Individual agent"""

        super().__init__(unique_id, model)

        # set constructor attributes
        self.reliability = reliability
        self.investigation_probability = investigation_probability
        self.philosophy = philosophy

        # initialize num_neighbors
        self.num_neighbors = self.model.num_neighbors

        # initialize truth_total
        self.num_facts = self.model.num_facts
        self.truth_total = 0

        #initialize all_facts
        self.all_facts = [0] * self.num_facts
        # initialize personal_facts
        self.initialize_personal_facts(self.num_facts, starting_knowledge)
        # initialize social_facts
        self.social_facts = [0] * self.num_facts
        # update all_facts
        self.update_all_facts()

        # initialize truth_total, false_total, truth_mean
        # unknown_personal_facts, unknown_social_facts, and unknown_total_facts
        self.update_true_false_unknown_counters()

    def update_true_false_unknown_counters(self) -> None:
        """Counts true, false, and unknown beliefs in personal_facts and
        social_facts. Saves these values in the proper attribute"""
        # make sure all_facts is up to date
        self.update_all_facts()
        # count 1's and -1's
        self.truth_total = self.all_facts.count(1)
        self.false_total = self.all_facts.count(-1)
        self.truth_mean = self.truth_total / (self.truth_total + self.false_total)

        self.unknown_personal_facts = self.personal_facts.count(0)
        self.unknown_social_facts = self.social_facts.count(0)
        self.unknown_total_facts = self.all_facts.count(0)

    def investigate(self) -> None:
        """Determines if agent observes something true or false about the
        world according to reliability. Adds belief to personal_facts"""
        index = self.get_random_index_of_abstained_belief()
        self.personal_facts[index] = self.get_belief()
        self.update_true_false_unknown_counters()

    def get_random_teachers(self) -> list:
        """Used by reid simulations. Returns list of n_neighbor random
        agents from whom this agent will solicit testimony"""
        teachers = []
        for i in range (self.num_neighbors):
            teacher = random.randint(0, self.model.num_agents)
            # make sure I didn't select myself
            while teacher == self.unique_id:
                teacher = random.randint(0, self.model.num_agents)
            teachers.append(teacher)
        return teachers

    def get_most_reliable_teachers(self) -> list:
        most_reliable_teacher_ids = get_max_n_indices(
            self.model.reliability_stats, self.num_neighbors)

        return most_reliable_teacher_ids

    def get_most_similar_teachers(self) -> list:
        my_agreement_list = [float(x) for x in self.model.agreement_stats[
            self.unique_id]]
        most_similar_teacher_ids = get_max_n_indices(my_agreement_list,
                                                     self.num_neighbors)
        return most_similar_teacher_ids

    def calculate_agreement(self, individual: Agent) -> float:
        """ Calculates the % of beliefs self has in common with individual"""
        my_beliefs = self.all_facts
        other_beliefs = individual.all_facts

        agreement_sum = 0
        disagreement_sum = 0
        for i in range(len(my_beliefs)):
            if my_beliefs[i] != 0 and other_beliefs[i] != 0:
                if my_beliefs[i] == other_beliefs[i]:
                    agreement_sum = agreement_sum + 1
                else:
                    disagreement_sum = disagreement_sum + 1

        if agreement_sum + disagreement_sum == 0:
            agreement_percent = 0
        else:
            agreement_percent = agreement_sum / (agreement_sum +
                                                 disagreement_sum)
        return agreement_percent


    def select_teachers(self) -> list:
        teachers = []
        if self.philosophy == "skeptical":
            # these individuals will not solicit testimony
            pass
        elif self.philosophy == "reid":
            # these individuals will solicit testimony randomly
            teachers = self.get_random_teachers()
        elif self.philosophy == "direct":
            # these individuals solicit testimony from others with highest
            # truth_mean
            teachers = self.get_most_reliable_teachers()
        elif self.philosophy == "indirect":
            # these individuals solicit testimony with others who have most
            # similar beliefs
            teachers = self.get_most_similar_teachers()
        return teachers

    def step(self) -> None:
        self.investigate()

        teachers = self.select_teachers()
        print(teachers)