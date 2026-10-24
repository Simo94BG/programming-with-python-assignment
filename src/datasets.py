import pandas as pd
from .database import engine
from .analyser import calculate_train_ideal_sse, find_best_ideal, assign_ideal_to_test
from .visualiser import plot_train_vs_chosen_ideal, plot_train_vs_chosen_ideal_deviation, plot_test_vs_chosen_ideal

class Dataset:
    def __init__(self, file_location, db_table, visualisation_path):
        self.file_location = file_location
        self.db_table = db_table
        self.visualisation_path = visualisation_path
        self.df = None

    def check_x_columns(self):
        if "x" not in self.df.columns:
            raise ErrorMissingXCol("No x column in dataset at location: " + self.file_location)

    def load_raw_to_df(self):
        try:
            self.df = pd.read_csv(str(self.file_location)) # type: ignore # because I am passing a string...
        except FileNotFoundError:
            raise FileNotFoundError("File not found at: " + str(self.file_location))

        self.check_x_columns() # Check if the dataset has an "x" column.

    def load_df_to_db(self):
        self.df.to_sql(self.db_table, engine, index=False, if_exists="replace")

    def load_from_db_to_df(self):
        self.df = pd.read_sql("SELECT * FROM " + self.db_table, engine)
        return self.df

class ResultDataset(Dataset):
    def __init__(self, db_table, df):
        super().__init__(file_location=None, db_table=db_table, visualisation_path=None)
        self.df = df

class IdealDataset(Dataset):
    def __init__(self, file_location, db_table):
        super().__init__(file_location, db_table, visualisation_path=None)

class TrainDataset(Dataset):
    def __init__(self, file_location, db_table, visualisation_path):
        super().__init__(file_location, db_table, visualisation_path)
        self.best_ideals_df = None

    def find_best_ideals(self, df_ideal):
        df_train = self.load_from_db_to_df()

        df_train_ideal_full_results = calculate_train_ideal_sse(df_train, df_ideal)
        train_ideal_full_results = ResultDataset("results_train_ideal_full_sse", df_train_ideal_full_results)
        train_ideal_full_results.load_df_to_db()
        best_ideals = ResultDataset("results_train_best_ideals", find_best_ideal(train_ideal_full_results.df))
        best_ideals.load_df_to_db()
        self.best_ideals_df = best_ideals.df

    def plot_best_ideals(self, df_ideal):
        plot_train_vs_chosen_ideal(self.df, df_ideal, self.best_ideals_df, self.visualisation_path)

    def plot_best_ideals_deviation(self, df_ideal):
        plot_train_vs_chosen_ideal_deviation(self.df, df_ideal, self.best_ideals_df, self.visualisation_path)

class TestDataset(Dataset):
    def __init__(self, file_location, db_table, visualisation_path):
        super().__init__(file_location, db_table, visualisation_path)
        self.mapped_df = None

    def map_ideals_to_test(self, df_ideal, df_mapping):
        mapped_test = ResultDataset("results_test_mapping" ,assign_ideal_to_test(self.df, df_ideal, df_mapping))
        mapped_test.load_df_to_db()
        self.mapped_df = mapped_test.df

    def plot_mapped_test(self):
        plot_test_vs_chosen_ideal(self.mapped_df, self.visualisation_path, mapped_only=True)
        plot_test_vs_chosen_ideal(self.mapped_df, self.visualisation_path, mapped_only=False)

class ErrorMissingXCol(Exception):
    """Raised when X column is missing in a dataframe"""
    pass