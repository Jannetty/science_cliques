from science_cliques.data_analysis import export_data
from science_cliques.model import CliqueModel


def run_og() -> None:
    """Mini runner to test cases from original paper"""
    run = 1
    num_neighbor_options = [2, 4, 6, 8]
    for num_neighbors in num_neighbor_options:
        num_neighbors
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
                    print(f"Run {run}, step {step}")

                # get summary statistics
                model.update_model_truth_false_mean_and_truth_false_total()
                print(f"Run {run}, {160 - run} runs remaining")
                run = run + 1
                export_data(model, "output_og.csv")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    """Main function that calls single run instance"""
    run_og()
