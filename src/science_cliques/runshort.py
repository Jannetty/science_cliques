from science_cliques.data_analysis import export_data
from science_cliques.model import CliqueModel


def run_short() -> None:
    """Mini runner to test single cases"""

    for replicate in range(1):
        model = CliqueModel(
            number_of_individuals=10,
            number_of_neighbors=8,
            num_facts=100,
            starting_knowledge=15,
            investigation_probability=0.1,
            skeptical=True,
        )
        for step in range(500):
            model.step()
            print(step)
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

        export_data(model, "short_output.csv")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    """Main function that calls single run instance"""
    run_short()
