# Module for the analysis functions
import numpy as np
import pandas as pd

# Calculate the sum of squared errors between two datasets
def calculate_sse(train_dataset, ideal_function):
    diff_squared = (train_dataset - ideal_function)**2 # Get the squared deviations per x value
    return sum(diff_squared) # Sum the squared deviations

def calculate_max_deviation(train_dataset, ideal_function):
    max_deviation = (train_dataset - ideal_function).abs().max()
    return max_deviation

def calculate_train_ideal_sse(train_df, ideal_df):
    # Make sure they're sorted by x so that there's no discrepancies
    # They both have 400 matching x values so just sorting should be ok here
    train_df = train_df.sort_values(by=['x'], ascending=True)
    ideal_df = ideal_df.sort_values(by=['x'], ascending=True)

    train_y_columns = train_df.drop(columns=['x']).columns
    ideal_y_columns = ideal_df.drop(columns=['x']).columns

    results = []

    for train_column in train_y_columns:

        for ideal_column in ideal_y_columns:
            # Deciding to calculate both the sse and max deviation in the same loop.
            # Might be more efficient to avoid unnecessary computation by calculating the max deviations later,
            # However, this is the cleanest way I could think of.
            calculated_sse = calculate_sse(train_df[train_column], ideal_df[ideal_column])
            calculated_max_deviation = calculate_max_deviation(train_df[train_column], ideal_df[ideal_column])

            # Append results to list
            results.append({
                "train_function": train_column
                ,"ideal_function": ideal_column
                ,"sse": calculated_sse
                ,"max_deviation": calculated_max_deviation
                ,"test_deviation_threshold": calculated_max_deviation * np.sqrt(2)
            })

    df_results = pd.DataFrame(results) # Convert results list to DataFrame
    return df_results

def find_best_ideal(df_train_ideal_results):
    # Use dataframe GROUP BY to find the MIN SSE for each train dataset
    best_ideals = df_train_ideal_results.loc[df_train_ideal_results.groupby("train_function")["sse"].idxmin()]
    return best_ideals

def assign_ideal_to_test(df_test, df_ideal, df_mapping):

    ideal_thresholds_dict = dict(zip(df_mapping["ideal_function"], df_mapping["test_deviation_threshold"]))
    results = []

    for _, row in df_test.iterrows(): # Don't need the index returned from iterrows, so _
        x_test = row["x"]
        y_test = row["y"]

        best_ideal = None
        best_ideal_y = None
        best_deviation = float('inf')
        #final_deviation = None

        for ideal_function, deviation_threshold in ideal_thresholds_dict.items():
            y_ideal = df_ideal.loc[df_ideal["x"] == x_test, ideal_function].values[0]
            deviation = abs(y_test - y_ideal)

            # Assignment instructions state "does not exceed" so <= threshold.
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
