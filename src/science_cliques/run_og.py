from science_cliques.data_analysis import export_data
from science_cliques.model import CliqueModel


def run_og(run_reps: bool, filename: str) -> None:
    """Mini runner to test cases from original paper"""
    num_neighbor_options = [2, 4, 6, 8]
    for num_neighbors in num_neighbor_options:
        if run_reps == True:
            iterate_through_philosophies_and_run(num_neighbors, True, filename)


def iterate_through_philosophies_and_run(num_neighbors: int, run_reps: bool, filename: str) -> None:
    """Runs original paper parameters with each philosophy"""
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
            run_for_ten_reps(num_neighbors, skeptical, reid, direct, indirect, filename)


def run_for_ten_reps(
    num_neighbors: int, skeptical: bool, reid: bool, direct: bool, indirect: bool, filename: str
) -> None:
    """Runs ten reps of the model for each set of parameters in original
    paper"""
    for replicate in range(10):
        model = CliqueModel(
            number_of_individuals=100,
            number_of_neighbors=num_neighbors,
            num_facts=1200,
            starting_knowledge=15,
            investigation_probability=0.1,
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
    """Main function that calls single run instance"""
    run_og(True, "output_og.csv")
