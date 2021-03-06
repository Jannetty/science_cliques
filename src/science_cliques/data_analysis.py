import csv
from science_cliques.model import CliqueModel


def export_data(model: CliqueModel, file_name: str) -> None:
    """Saves all parameteres and outputs of model run"""
    # get parameters
    num_individuals = str(model.num_agents)
    num_neighbors = str(model.num_neighbors)
    num_facts = str(model.num_facts)
    starting_knowledge = str(model.starting_knowledge)
    investigation_probability = str(model.investigation_probability)
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
    print(f"Investigation Probability {investigation_probability}")
    print(f"Philosophy: {philosophy}")
    print(f"Truth mean: {truth_mean}")
    print(f"Truth total: {truth_total}")
    print(f"False mean: {false_mean}")
    print(f"False total: {false_total}")
    print("-----------------------------------")
    newrow = [
        num_individuals,
        num_neighbors,
        num_facts,
        starting_knowledge,
        investigation_probability,
        philosophy,
        truth_mean,
        truth_total,
        false_mean,
        false_total,
    ]

    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object

    file_path = "data/" + file_name
    with open(file_path, "a", newline="\n") as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = csv.writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(newrow)
        # Close the file object
        f_object.close()
