# from mesa import Agent, Model
import numpy as np
from science_cliques.model import CliqueModel
from science_cliques.data_analysis import export_data


def run() -> None:
    """Runs the model with all parameter values of interest"""
    # Possible ranges of parameters
    # possible_number_of_neighbors = [2, 4, 6, 8] # len 4
    possible_number_of_neighbors = [8]  # len 1

    possible_number_of_individuals_range = range(20, 101, 20)
    possible_number_of_individuals = [8]
    for i in possible_number_of_individuals_range:
        possible_number_of_individuals.append(i)  # len 6

    possible_number_of_facts_range = range(300, 1501, 300)
    possible_number_of_facts = [16]  # to be greater than starting_knowledge
    for i in possible_number_of_facts_range:
        possible_number_of_facts.append(i)  # len 6

    possible_investigation_probability = np.arange(0, 1, 0.2)  # len 5
    # could be interesting to see possible starting knowledge
    # possible_starting_knowledge = range(0, 1501, 300) # len 6
    # possible_reliability_alpha = range(1, 101)
    # possible_reliability_beta = np.arange(0.001, 0.991, 0.01)

    run_number = 1
    total_runs = 7200

    for num_neighbors in possible_number_of_neighbors:
        for number_of_individuals in possible_number_of_individuals:
            for number_of_facts in possible_number_of_facts:
                for investigation_probability in possible_investigation_probability:
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

                            run_number = run_number + 1
                            print(
                                f"Run number: {run_number}, {total_runs - run_number} "
                                f"runs remaining."
                            )
                            export_data(model, "output.txt")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
