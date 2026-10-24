from .datasets import IdealDataset, TrainDataset, TestDataset
from .setup import initial_setup

datasets_path = "data/"
ideal_file_name = "ideal.csv"
train_file_name = "train.csv"
test_file_name = "test.csv"
visualisations_path = "visualisations/"

if __name__ == "__main__":
    print("Running Initial Setup...")
    initial_setup()

    # 1. Create Dataset Objects
    ideal = IdealDataset(datasets_path + ideal_file_name, "raw_ideal")
    train = TrainDataset(datasets_path + train_file_name, "raw_train", visualisations_path)
    test = TestDataset(datasets_path + test_file_name, "raw_test", visualisations_path)
    objects_list = [ideal, train, test]

    # 2. Load Raw Data from CSV to DF to Database
    for obj in objects_list:
        obj.load_raw_to_df()
        obj.load_df_to_db()

    # 3. Find Best Ideal
    train.find_best_ideals(ideal.df)
    train.plot_best_ideals(ideal.df)

    # 4. Map Test Data
    test.map_ideals_to_test(ideal.df, train.best_ideals_df)
    test.plot_mapped_test()