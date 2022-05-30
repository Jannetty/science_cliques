from mesa import Agent
from model import Model


class Individual(Agent):
    """Individual Agent

    ...
    Constructor parameters


    ...
    Attributes
    ---
        unique_id : int
            unique agent identifier

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

        unknown_personal_facts : int
            number of personal facts that have value 0

        unknown_total_facts : int
            number of facts that have value 0 in both personal_facts and
            social_facts

        truth total : int
            total number of beliefs that have value 1

        truth mean : float
            (number of beliefs that have value == 1) / ((number of beliefs that
            have value == 1) + (number of beliefs that have values == -1))

        reliability : float
            agent's private reliability. Drawn from beta distribution alpha = 1.5,
            beta = 1 (so average across population is .6)

        personal_rewire : int
            agent's rewire probability. 0 if model reid or skeptical = 0,
            otherwise 1.

        investigation_probability : float
            defaults to .1. Probability an agent observes something true about
            the world on each run.

        index : array I think
            used in indirect_calibration_rewire to order agents who have highest
            agreement with this agent. I don't think we actually need this
            parameter but we'll see.

    ...

    Functions
    ---



    """

    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.starting_knowledge = 10

    def step(self) -> None:
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        print("Hi, I am agent " + str(self.unique_id) + ".")
