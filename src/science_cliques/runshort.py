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

    with open("output.csv", "a", newline="\n") as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = csv.writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(newrow)
        # Close the file object
        f_object.close()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    for i in range(10):
        model = CliqueModel(skeptical=True, number_of_individuals=10)

        for i in range(500):
            print(i)
            model.step()

        # get summary statistics
        model.update_model_truth_false_mean_and_truth_false_total()
        truth_mean = model.truth_mean
        truth_total = model.total_truth
        false_mean = model.false_mean
        false_total = model.total_false

        print(f"Truth mean: {truth_mean}")
        print(f"Truth total: {truth_total}")
        print(f"False mean: {false_mean}")
        print(f"False total: {false_total}")
