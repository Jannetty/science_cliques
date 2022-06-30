# from mesa import Agent, Model
import numpy as np
from science_cliques.model import CliqueModel
from science_cliques.data_analysis import export_data


def run(run_reps: bool, filename: str) -> None:
    """Setus up all number_of_neighbor values of interest"""
    possible_number_of_neighbors = [8]
    for num_neighbors in possible_number_of_neighbors:
        run_with_each_num_neighbors(num_neighbors, run_reps, filename)


def run_with_each_num_neighbors(num_neighbors: int, run_reps: bool, filename: str) -> None:
    """Sets up all number_of_individual values of interest"""
    # make array of possible number of individuals
    possible_number_of_individuals_range = range(20, 101, 20)
    possible_number_of_individuals = [8]
    for i in possible_number_of_individuals_range:
        possible_number_of_individuals.append(i)  # len 6
    for number_of_individuals in possible_number_of_individuals:
        run_with_each_num_individuals(num_neighbors, number_of_individuals, run_reps, filename)


def run_with_each_num_individuals(
    num_neighbors: int, number_of_individuals: int, run_reps: bool, filename: str
) -> None:
    """Sets up all num_facts values of interest"""
    # make array of possible number of facts
    possible_number_of_facts_range = range(300, 1501, 300)
    possible_number_of_facts = [16]  # to be greater than starting_knowledge
    for i in possible_number_of_facts_range:
        possible_number_of_facts.append(i)  # len 6
    for number_of_facts in possible_number_of_facts:
        run_with_each_number_of_facts(
            num_neighbors, number_of_individuals, number_of_facts, run_reps, filename
        )


def run_with_each_number_of_facts(
    num_neighbors: int,
    number_of_individuals: int,
    number_of_facts: int,
    run_reps: bool,
    filename: str,
) -> None:
    """Sets up all investigion_probability values of interest"""
    # make array of possible investigation probabilities
    possible_investigation_probability = np.arange(0, 1, 0.2)  # len 5
    for investigation_probability in possible_investigation_probability:
        run_with_each_invest_probability(
            num_neighbors,
            number_of_individuals,
            number_of_facts,
            investigation_probability,
            run_reps,
            filename,
        )


def run_with_each_invest_probability(
    num_neighbors: int,
    number_of_individuals: int,
    number_of_facts: int,
    investigation_probability: float,
    run_reps: bool,
    filename: str,
) -> None:
    """Iterates through each philosophy with previously defined parameter
    values"""
    for philosophy in range(4):
        if philosophy == 0:
            skeptical = True
            reid = False
            direct = False
            indirect = False
        if philosophy == 1:
            skeptical = False
            reid = True
            direct = False
            indirect = False
        if philosophy == 2:
            skeptical = False
            reid = False
            direct = True
            indirect = False
        if philosophy == 3:
            skeptical = False
            reid = False
            direct = False
            indirect = True

        if run_reps is True:
            run_ten_reps(
                num_neighbors,
                number_of_individuals,
                number_of_facts,
                investigation_probability,
                skeptical,
                reid,
                direct,
                indirect,
                filename,
            )


def run_ten_reps(
    num_neighbors: int,
    number_of_individuals: int,
    number_of_facts: int,
    investigation_probability: float,
    skeptical: bool,
    reid: bool,
    direct: bool,
    indirect: bool,
    filename: str,
) -> None:
    """Runs ten reps of model with previously defined parameter options"""
    for model_replicate in range(10):
        model = CliqueModel(
            number_of_individuals=number_of_individuals,
            number_of_neighbors=num_neighbors,
            num_facts=number_of_facts,
            investigation_probability=investigation_probability,
            skeptical=skeptical,
            reid=reid,
            direct=direct,
            indirect=indirect,
        )

        for step in range(500):
            model.step()

        # get summary statistics
        model.update_model_truth_false_mean_and_truth_false_total()

        export_data(model, filename)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    """Runs full model iterating through all parameter options of interest"""
    run(True, "output.txt")
