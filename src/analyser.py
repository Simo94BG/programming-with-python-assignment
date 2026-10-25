"""
Module containing all analysis functions.
Contains both basic and higher level functions. Basic functions include calculation of SSE, Max Deviation and others.
The higher level functions find the best ideal functions for training datasets,
and also map the chosen ideal functions to the test data records.
"""

import pandas as pd

# Calculate the sum of squared errors between two datasets
def calculate_sse(train_dataset, ideal_function):
    diff_squared = (train_dataset - ideal_function)**2 # Get the squared deviations per x value
    return sum(diff_squared) # Sum the squared deviations

# Calculate the max absolute deviation between two datasets
def calculate_max_deviation(train_dataset, ideal_function):
    max_deviation = (train_dataset - ideal_function).abs().max()
    return max_deviation

def calculate_train_ideal_sse(train_df, ideal_df, threshold_factor):

    """
    Function which loops through each train & ideal dataset pair, and calculates their:
    - SSE
    - Max Deviation
    - Deviation Threshold

    :param train_df: DataFrame containing the training dataset.
    :param ideal_df: DataFrame containing the ideal functions dataset.
    :param threshold_factor: Value/Formula of the deviation threshold factor (for mapping the ideals to the test data).
    :return: DataFrame of all train & ideal function pairs, along with the calculated data for each pair.
    """

    # Make sure the datasets are sorted by x so that there's no discrepancies (again, to be extra safe)
    train_df = train_df.sort_values(by=['x'], ascending=True)
    ideal_df = ideal_df.sort_values(by=['x'], ascending=True)

    # Once datasets are matched by x, drop the x columns, so that we're left with only the y columns to loop through.
    train_y_columns = train_df.drop(columns=['x']).columns
    ideal_y_columns = ideal_df.drop(columns=['x']).columns

    results = []

    for train_column in train_y_columns:

        for ideal_column in ideal_y_columns:

            """
            Deciding to calculate both the sse and max deviation in the same loop.
            Might be more efficient to avoid unnecessary computation by calculating the max deviations later,
            However, this is a cleaner way and provides more data for extra analysis, if required.
            """

            calculated_sse = calculate_sse(train_df[train_column], ideal_df[ideal_column])
            calculated_max_deviation = calculate_max_deviation(train_df[train_column], ideal_df[ideal_column])

            # Append results to list
            results.append({
                "train_function": train_column
                ,"ideal_function": ideal_column
                ,"sse": calculated_sse
                ,"max_deviation": calculated_max_deviation
                ,"test_deviation_threshold": calculated_max_deviation * threshold_factor
            })

    df_results = pd.DataFrame(results) # Convert results list to DataFrame
    return df_results

def find_best_ideal(df_train_ideal_results):
    # Use dataframe GROUP BY to find the MIN SSE for each train dataset
    best_ideals = df_train_ideal_results.loc[df_train_ideal_results.groupby("train_function")["sse"].idxmin()]
    return best_ideals

def assign_ideal_to_test(df_test, df_ideal, df_mapping):

    """
    Function to map the test dataset's record to one of the chosen ideal functions
    It loops through each line in the test dataset.
        Within each line in the test dataset, it loops through each chosen ideal function.
            For each of the chosen ideal functions, it compares the deviation against the test value.
            If the deviation against the test value is below the specified threshold,
            and it is also lower than the current best deviation:
            It will choose the current ideal function as the best match to this test record (line).
        Once all chosen ideal functions have been looped through, the best ideal function is left (if any).

    Unmapped test values are kept for now, and a separate dataset without them is created at a later stage.
    :param df_test: Test Dataset DataFrame
    :param df_ideal: Ideal Dataset DataFrame
    :param df_mapping: DataFrame containing the chosen ideal functions, including other data such as max thresholds.
    :return: DataFrame containing the test dataset with the additional mapped ideal function data.
    """

    # Prepare a dictionary with the mapping thresholds for each chosen ideal function.
    ideal_thresholds_dict = dict(zip(df_mapping["ideal_function"], df_mapping["test_deviation_threshold"]))
    results = []

    # For each row in the test dataset...
    for _, row in df_test.iterrows(): # Don't need the index returned from iterrows, so _
        x_test = row["x"]
        y_test = row["y"]

        best_ideal = None
        best_ideal_y = None
        best_deviation = float('inf') # Start at infinity, so that any value within the threshold will be picked.

        # For each ideal function (and its deviation threshold)...
        for ideal_function, deviation_threshold in ideal_thresholds_dict.items():
            y_ideal = df_ideal.loc[df_ideal["x"] == x_test, ideal_function].values[0]
            deviation = abs(y_test - y_ideal) # Deviation between the test and the ideal function's y values.

            # If the deviation <= the deviation threshold. Requirements state "does not exceed" so <= threshold.
            if deviation <= deviation_threshold and deviation < best_deviation:
                best_ideal = ideal_function
                best_ideal_y = y_ideal
                best_deviation = deviation

        # If best_deviation stayed as infinity, replace with None, since we don't want infinity in the database.
        best_deviation = None if best_deviation == float('inf') else best_deviation

        results.append({
            "x_test": x_test,
            "y_test": y_test,
            "y_ideal": best_ideal_y,
            "deviation": best_deviation
            ,"ideal_function": best_ideal
        })

    return pd.DataFrame(results)
