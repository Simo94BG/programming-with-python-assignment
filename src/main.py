"""
Main module of the Datasets solution.
This solution finds the best ideal function (from the provided ideal functions dataset) for each training dataset.
After that, it also maps the best ideal function to each record of the test dataset, provided that it meets the threshold.
The solution also generates visualisations to aid with analysis.
All results are stored in a SQLite database located in the "data" folder of this solution.

This main module runs the full process:
- Initial Setup: Re-set up the SQLite database
- Load raw CSV datasets into the database.
- Find the best ideal functions for each training dataset, and produce helpful visualisations.
- Map each test data record to one of the chosen ideal functions (from the previous step), and produce visualisations.

All configuration values are managed by the 6 variables below
"""

from .datasets import IdealDataset, TrainDataset, TestDataset
from .setup import initial_setup

datasets_path = "data/" # Folder location of the raw datasets. Database will be stored in "data".
ideal_file_name = "ideal.csv"
train_file_name = "train.csv"
test_file_name = "test.csv"
visualisations_path = "visualisations/" # Folder location for the generated visualisations.
test_mapping_threshold_factor = 2 ** 0.5 # Test mapping threshold factor. 2 ** 0.5 == sqrt(2) (square root of 2)

if __name__ == "__main__":
    print("Running Initial Setup...")
    initial_setup()

    # 1. Create Dataset Objects
    ideal = IdealDataset(datasets_path + ideal_file_name, "raw_ideal")
    train = TrainDataset(datasets_path + train_file_name, "raw_train", visualisations_path, test_mapping_threshold_factor)
    test = TestDataset(datasets_path + test_file_name, "raw_test", visualisations_path)
    datasets_list = [ideal, train, test]

    # 2. Load Raw Data from CSVs to DataFrames and write them to the Database
    for dataset in datasets_list:
        dataset.load_raw_to_df()
        dataset.load_df_to_db()

    # 3. Find the best ideals and plot against the training data
    train.find_best_ideals(ideal.df)
    train.plot_best_ideals(ideal.df)
    train.plot_best_ideals_deviation(ideal.df)

    # 4. Map the test data and plot the ideals mapped to the test data
    test.map_ideals_to_test(ideal.df, train.best_ideals_df)
    test.plot_mapped_test()