from science_cliques.model import CliqueModel


def run_short() -> None:
    """Mini runner to test single cases"""
    for i in range(10):
        model = CliqueModel(skeptical=True, number_of_individuals=10)

        for j in range(50):
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


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    """Main function that calls single run instance"""
    run_short()
