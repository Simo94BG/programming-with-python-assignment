import os
from database import Base, engine
import sqlalchemy as sa
from loader import load_raw_data
import pandas as pd

RUN_INITIAL_SETUP = True

def initial_setup():
    # For now using OS to remove the db file, as it's easier.
    # Maybe later could update to use models.py and create the ORM models, which would allow to drop the tables.
    #if os.path.exists("written_assignment.db"):
    #    os.remove("written_assignment.db")
    #    print("Old database deleted...")

    # Using DROP table through a direct SQL for now as it's easier.
    # Maybe later could update to use models.py and create the ORM models, which would allow to drop the tables.
    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS raw_ideal"))
        conn.execute(sa.text("DROP TABLE IF EXISTS raw_train"))
        conn.execute(sa.text("DROP TABLE IF EXISTS raw_test"))

    Base.metadata.create_all(bind=engine)
    print("Database re-created at:", engine.url, "...")

    print("Loading Raw Data...")
    raw_data_list = ["ideal", "train", "test"]
    for raw_data_item in raw_data_list:
        load_raw_data(raw_data_item)
    print("Raw Data Loaded Successfully!")
    print("Initial Setup Completed.")

def load_raw_from_database():
    df_ideal_sql = pd.read_sql("SELECT * FROM raw_ideal", engine)
    df_train_sql = pd.read_sql("SELECT * FROM raw_train", engine)
    return df_ideal_sql, df_train_sql

# Calculate the sum of squared errors between two datasets
def calculate_sse(train_dataset, ideal_function):
    diff_squared = (train_dataset - ideal_function)**2 # Get the squared deviations per x value
    return sum(diff_squared) # Sum the squared deviations

def find_best_ideal(train_df, ideal_df):
    # Make sure they're sorted by x so that there's no discrepancies
    # They both have 400 matching x values so just sorting should be ok here
    train_df = train_df.sort_values(by=['x'], ascending=True)
    ideal_df = ideal_df.sort_values(by=['x'], ascending=True)

    train_y_columns = train_df.drop(columns=['x']).columns
    ideal_y_columns = ideal_df.drop(columns=['x']).columns

    results = {}

    for train_column in train_y_columns:
        lowest_sse = float("inf")
        ideal_function = None


        for ideal_column in ideal_y_columns:
            calculated_sse = calculate_sse(train_df[train_column], ideal_df[ideal_column])
            if calculated_sse < lowest_sse:
                lowest_sse = calculated_sse
                ideal_function = ideal_column

        results[train_column] = [ideal_function, lowest_sse]

        # This is fine, but what would be better is to store each train vs ideal sse, and plot them.

    return results

if __name__ == "__main__":
    if RUN_INITIAL_SETUP:
        print("Re-running Initial Setup...")
        initial_setup()

    df_ideal, df_train = load_raw_from_database()

    print(find_best_ideal(df_train, df_ideal))