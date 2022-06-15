# from mesa import Agent, Model
from science_cliques.model import CliqueModel

# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    model = CliqueModel(indirect=True, number_of_individuals=10)

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