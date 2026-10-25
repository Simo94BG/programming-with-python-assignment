"""
Datasets module providing functionality to work with the different required datasets.
Functionality includes:
 - Loading raw CSV files to dataframes.
 - Saving dataset dataframes to the database.
 - Computing results and performing comparisons between the datasets.
 - Plotting interactive visualisations of the results.
"""

import pandas as pd
from .database import engine
from .analyser import calculate_train_ideal_sse, find_best_ideal, assign_ideal_to_test
from .visualiser import plot_train_vs_chosen_ideal, plot_train_vs_chosen_ideal_deviation, plot_test_vs_chosen_ideal

class Dataset:

    """
    Base dataset class providing shared functionality for working with datasets from CSV files.
    Provides ability to load from CSV to Dataframes, save Dataframes to the Database.
    Also performs basic checks.
    """

    def __init__(self, file_location, db_table, visualisation_path):
        self.file_location = file_location
        self.db_table = db_table
        self.visualisation_path = visualisation_path
        self.df = None

    def check_x_columns(self):
        # Ensure the dataset has an 'x' column
        if "x" not in self.df.columns:
            raise ErrorMissingXCol("No x column in dataset at location: " + self.file_location)

    def load_raw_to_df(self):
        # Try load the raw CSV file, and if not found raise a standard File Not Found Error.
        try:
            self.df = pd.read_csv(str(self.file_location)) # type: ignore # because I am passing a string...
        except FileNotFoundError:
            raise FileNotFoundError("File not found at: {self.file_location}" + str(self.file_location))

        self.check_x_columns() # Check if the dataset has an "x" column.

    def load_df_to_db(self):
        self.df.to_sql(self.db_table, engine, index=False, if_exists="replace") # Overwrites the table if it exists

    def load_from_db_to_df(self):
        self.df = pd.read_sql("SELECT * FROM " + self.db_table, engine)
        return self.df

class ResultDataset(Dataset):

    """
    Class for output datasets.
    Allows to store result/output datasets as objects, and work with their dataframes.
    File Location and Visualisation Path are not required, so they are not inherited from the Dataset class.
    """

    def __init__(self, db_table, df):
        super().__init__(file_location=None, db_table=db_table, visualisation_path=None)
        self.df = df

class IdealDataset(Dataset):

    """
    Class for the dataset containing Ideal Functions.
    No extra functionality added to the base Dataset class, but exists for clarity and future extensibility.
    No visualisations are generated, so the Visualisation Path is not required and not inherited from Dataset.
    """

    def __init__(self, file_location, db_table):
        super().__init__(file_location, db_table, visualisation_path=None)

class TrainDataset(Dataset):

    """
    Class for the dataset containing the training data. Inherits all functionality from parent class Dataset.
    Provides further functionality for finding the best ideal function for each training dataset,
    as well as interactive chart plotting functionality.
    """

    def __init__(self, file_location, db_table, visualisation_path, threshold_factor):
        super().__init__(file_location, db_table, visualisation_path)
        self.best_ideals_df = None
        self.threshold_factor = threshold_factor

    def find_best_ideals(self, df_ideal):

        """
        Finds the best ideal function for each training dataset.

        Firstly, it sorts both datasets by x, and then compares their x values to ensure they're exactly the same.
        This is because if the x values of the datasets are different, the program will return incorrect results.

        Secondly, it computes the SSE (sum of squared errors) between each training dataset and ideal function
        The full SSE results are stored in a ResultDataset class and in the database.

        Lastly, the ideal function with the lowest SSE for each training dataset is found.
        The best matching train & ideal pairs are also stored in a separate ResultsDataset class and database table.

        :param df_ideal: DataFrame containing the ideal functions dataset.
        :return: None
        """

        df_train = self.load_from_db_to_df()

        # Sort both datasets by x, to ensure they're not mismatched.
        df_train = df_train.sort_values(by="x").reset_index(drop=True)
        df_ideal = df_ideal.sort_values(by="x").reset_index(drop=True)

        # Now that they're sorted by x, perform an extra check to ensure the values are indeed matching.
        if not df_train["x"].equals(df_ideal["x"]):
            raise ValueError("Training and Ideal datasets must have an identical set of x-values")

        # Calculate the SSE between each training dataset & ideal function pair.
        df_train_ideal_full_results = calculate_train_ideal_sse(df_train, df_ideal, self.threshold_factor)
        train_ideal_full_results = ResultDataset("results_train_ideal_full_sse", df_train_ideal_full_results)
        train_ideal_full_results.load_df_to_db() # Load full SSE results to database

        # Find the best ideals for each training dataset by filtering for the lowest SSE.
        best_ideals = ResultDataset("results_train_best_ideals", find_best_ideal(train_ideal_full_results.df))
        best_ideals.load_df_to_db() # Load best training & ideal pairs to database.
        self.best_ideals_df = best_ideals.df # Apply best training & ideal pairs to instance dataframe for later use.

    def plot_best_ideals(self, df_ideal):
        plot_train_vs_chosen_ideal(self.df, df_ideal, self.best_ideals_df, self.visualisation_path)

    def plot_best_ideals_deviation(self, df_ideal):
        plot_train_vs_chosen_ideal_deviation(self.df, df_ideal, self.best_ideals_df, self.visualisation_path)

class TestDataset(Dataset):

    """
    Class for the test dataset containing the test data. Inherits all functionality from the parent class Dataset.
    Provides further functionality for mapping the chosen ideal functions (from the training dataset) to
    each of the test dataset's records, as long as they are below the specified threshold.
    Also provides plotting functionality to plot the mapped ideal functions against the test data - for both the
    full test dataset, as well as only the mapped values.
    """

    def __init__(self, file_location, db_table, visualisation_path):
        super().__init__(file_location, db_table, visualisation_path)
        self.df_mapped_full = None
        self.df_mapped_only = None

    def map_ideals_to_test(self, df_ideal, df_mapping):

        """
        Run through each test data record and map it against the best matching  ideal function,
        provided that the deviation is below the specified threshold.
        :param df_ideal: DataFrame of the ideal functions.
        :param df_mapping: DataFrame of the mapping between the training dataset and chosen ideal functions.
        :return: None
        """

        # The map the full test dataset to the chosen ideal functions
        test_mapped_full = ResultDataset("results_test_mapping_full" ,assign_ideal_to_test(self.df, df_ideal, df_mapping))
        test_mapped_full.load_df_to_db()
        self.df_mapped_full = test_mapped_full.df # Store as Dataframe to use in chart plotting later.

        # Filter the full test mapping dataset and only keep the mapped ones.
        df_test_mapped_only = test_mapped_full.df[test_mapped_full.df["ideal_function"].notna()]
        test_mapped_only = ResultDataset("results_test_mapping", df_test_mapped_only)
        test_mapped_only.load_df_to_db()
        self.df_mapped_only = test_mapped_only.df # Store as Dataframe to use in chart plotting later.

    def plot_mapped_test(self):
        plot_test_vs_chosen_ideal(self.df_mapped_only, self.visualisation_path, mapped_only=True)
        plot_test_vs_chosen_ideal(self.df_mapped_full, self.visualisation_path, mapped_only=False)

class ErrorMissingXCol(Exception):
    """Raised when the X column is missing in a dataframe"""
    pass