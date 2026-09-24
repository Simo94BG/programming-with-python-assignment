import os
from database import Base, engine
from loader import load_raw_data

RUN_INITIAL_SETUP = True

def initial_setup():
    # For now using OS to remove the db file, as it's easier.
    # Maybe later could update to use models.py and create the ORM models, which would allow to drop the tables.
    if os.path.exists("written_assignment.db"):
        os.remove("written_assignment.db")
        print("Old database deleted...")

    Base.metadata.create_all(bind=engine)
    print("Database re-created at:", engine.url, "...")

    print("Loading Raw Data...")
    raw_data_list = ["ideal", "train", "test"]
    for raw_data_item in raw_data_list:
        load_raw_data(raw_data_item)
    print("Raw Data Loaded Successfully!")
    print("Initial Setup Completed.")

if __name__ == "__main__":
    if RUN_INITIAL_SETUP:
        print("Re-running Initial Setup...")
        initial_setup()
    # INITIAL SETUP SEEMS TO BE COMPLETED. MOVE ON TO NEXT STEPS FOR NOW.