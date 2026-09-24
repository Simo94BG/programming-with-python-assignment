import pandas as pd
from database import engine

raw_data_list = ["ideal", "train", "test"]

def load_raw_data(raw_dataset):
    df = pd.read_csv(raw_dataset + ".csv")
    # Using df.to_sql() to load the data as it's much easier than setting up the ORM models.
    # Maybe later will change it...
    df.to_sql("raw_" + raw_dataset, engine, index=False, if_exists="replace")
    return df