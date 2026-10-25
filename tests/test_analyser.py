"""
Unit test module for the analyser module.
Performs unit tests of the high level functions in the analyser module,
because they contain the most critical logic in the whole program - calculating the results.

Manual data and manually calculated (and verified) results are added to variables below.
Results are manually calculated, in order to avoid re-using any of the existing analyser logic.
"""

import pandas as pd
from src.analyser import calculate_sse, calculate_max_deviation, calculate_train_ideal_sse, assign_ideal_to_test

# Manually input test data
df_train_manual = pd.DataFrame({
    "x": [1, 2, 3],
    "y_train": [10, 20, 30]
})

df_ideal_manual = pd.DataFrame({
    "x": [1, 2, 3],
    "ideal_1": [11, 21, 31],
    "ideal_2": [14, 24, 34]
})

df_test_manual = pd.DataFrame({
    "x": [1, 2, 3]
    ,"y": [10, 20, 25]
})

# Manually input expected results
expected_sse_manual = {
    "ideal_1_sse": 3
    ,"ideal_2_sse": 48
}

expected_max_deviation_manual = {
    "ideal_1_max_dev": 1
    ,"ideal_2_max_dev": 4
}

expected_ideal_manual = "ideal_1"

df_expected_train_ideal_mapping_manual = pd.DataFrame({
    "train_function": ["y_train", "y_train"]
    ,"ideal_function": ["ideal_1", "ideal_2"]
    ,"sse": [3, 48]
    ,"max_deviation": [1, 4]
    ,"test_deviation_threshold": [1.41421, 5.65685]
})

df_expected_test_mapping_manual = pd.DataFrame({
    "x_test": [1, 2, 3]
    ,"y_test": [10, 20, 25]
    ,"y_ideal": [11, 21, None]
    ,"deviation": [1, 1, None]
    ,"ideal_function": ["ideal_1", "ideal_1", None]
})

def test_sse(df_train, df_ideal, dict_expected_results):
    """
    Test the SSE function
    :param df_train: DataFrame containing the unit-test's training dataset.
    :param df_ideal: DataFrame containing the unit-test's ideal functions dataset.
    :param dict_expected_results: Dictionary containing the expected results of the unit-test.
    :return: None
    """

    y_train_col = df_train["y_train"]
    y_ideal_1 = df_ideal["ideal_1"]
    y_ideal_2 = df_ideal["ideal_2"]
    expected_sse_1 = dict_expected_results["ideal_1_sse"]
    expected_sse_2 = dict_expected_results["ideal_2_sse"]

    assert calculate_sse(y_train_col, y_ideal_1) == expected_sse_1
    assert calculate_sse(y_train_col, y_ideal_2) == expected_sse_2
    print("SSE Calculation Test Passed...")

def test_max_deviation(df_train, df_ideal, dict_expected_results):
    """
    Test the Max Deviation function
    :param df_train: DataFrame containing the unit-test's training dataset.
    :param df_ideal: DataFrame containing the unit-test's ideal functions dataset.
    :param dict_expected_results: Dictionary containing the expected results of the unit-test.
    :return: None
    """

    y_train_col = df_train["y_train"]
    y_ideal_1 = df_ideal["ideal_1"]
    y_ideal_2 = df_ideal["ideal_2"]

    expected_max_dev_1 = dict_expected_results["ideal_1_max_dev"]
    expected_max_dev_2 = dict_expected_results["ideal_2_max_dev"]

    assert calculate_max_deviation(y_train_col, y_ideal_1) == expected_max_dev_1
    assert calculate_max_deviation(y_train_col, y_ideal_2) == expected_max_dev_2
    print("Max Deviation Calculation Test Passed...")

def test_train_ideal_full_results(df_train, df_ideal, df_expected_result):
    """
    Test the function which finds the best ideal functions for each training dataset.
    :param df_train: DataFrame containing the unit-test's training dataset.
    :param df_ideal: DataFrame containing the unit-test's ideal functions dataset.
    :param df_expected_result: DataFrame containing the expected results of the unit-test.
    :return: None
    """

    df_returned_result = calculate_train_ideal_sse(df_train, df_ideal, threshold_factor=2**0.5)

    # Round the deviation threshold column, to make it easier to type in the manual result at the top
    df_returned_result["test_deviation_threshold"] = df_returned_result["test_deviation_threshold"].round(5)

    pd.testing.assert_frame_equal(df_returned_result, df_expected_result) # Pandas assert to compare dataframes.
    print("Train Ideal Full Results Function Test Passed...")

def test_assign_ideal_to_test(df_test, df_ideal, df_mapping, df_expected_result):
    """
    Test the function which maps the ideal functions to each test dataset record.
    :param df_test: DataFrame containing the unit-test's test dataset.
    :param df_ideal: DataFrame containing the unit-test's ideal functions dataset.
    :param df_mapping: DataFrame containing the unit-test's mapping between the training dataset and ideal functions.
    :param df_expected_result: DataFrame containing the expected results of the unit-test.
    :return: None
    """

    df_returned_result = assign_ideal_to_test(df_test, df_ideal, df_mapping)
    pd.testing.assert_frame_equal(df_returned_result, df_expected_result)
    print("Map Ideal to Test Function Test Passed...")

# Run the unit test functions below.
test_sse(df_train_manual, df_ideal_manual, expected_sse_manual)
test_max_deviation(df_train_manual, df_ideal_manual, expected_max_deviation_manual)
test_train_ideal_full_results(df_train_manual, df_ideal_manual, df_expected_train_ideal_mapping_manual)
test_assign_ideal_to_test(
    df_test_manual
    ,df_ideal_manual
    ,df_expected_train_ideal_mapping_manual
    ,df_expected_test_mapping_manual
)
print("All Analyser Tests Passed!")