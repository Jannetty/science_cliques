# from mesa import Agent, Model
import csv
import numpy as np
from science_cliques.model import CliqueModel


def export_data(model: CliqueModel) -> None:
    """Saves all parameteres and outputs of model run"""
    # get parameters
    num_individuals = str(model.num_agents)
    num_neighbors = str(model.num_neighbors)
    num_facts = str(model.num_facts)
    starting_knowledge = str(model.starting_knowledge)
    philosophy = str(model.philosophy)

    # get summary statistics
    model.update_model_truth_false_mean_and_truth_false_total()
    truth_mean = str(model.truth_mean)
    truth_total = str(model.total_truth)
    false_mean = str(model.false_mean)
    false_total = str(model.total_false)

    # export to csv
    print(f"Number of Individuals: {num_individuals}")
    print(f"Number of Neighbors: {num_neighbors}")
    print(f"Number of Facts: {num_facts}")
    print(f"Starting Knowledge: {starting_knowledge}")
    print(f"Philosophy: {philosophy}")
    print(f"Truth mean: {truth_mean}")
    print(f"Truth total: {truth_total}")
    print(f"False mean: {false_mean}")
    print(f"False total: {false_total}")
    newrow = [
        num_individuals,
        num_neighbors,
        num_facts,
        starting_knowledge,
        philosophy,
        truth_mean,
        truth_total,
        false_mean,
        false_total,
    ]

    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object

    with open("data/output.csv", "a", newline="\n") as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = csv.writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(newrow)
        # Close the file object
        f_object.close()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    # Possible ranges of parameters
    # possible_number_of_neighbors = [2, 4, 6, 8] # len 4
    possible_number_of_neighbors = [8]  # len 1

    possible_number_of_individuals_range = range(20, 101, 20)
    possible_number_of_individuals = [8]
    for i in possible_number_of_individuals_range:
        possible_number_of_individuals.append(i)  # len 6

    possible_number_of_facts_range = range(300, 1501, 300)
    possible_number_of_facts = [1]
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

                        for i in range(10):
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

                            for i in range(500):
                                print(i)
                                model.step()

                            # get summary statistics
                            model.update_model_truth_false_mean_and_truth_false_total()
                            truth_mean = model.truth_mean
                            truth_total = model.total_truth
                            false_mean = model.false_mean
                            false_total = model.total_false

                            run_number = run_number + 1
                            print(
                                f"Run number: {run_number}, {total_runs - run_number} "
                                f"runs remaining."
                            )
                            export_data(model)
