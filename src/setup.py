"""
Initial setup module.
Creates the db file if it doesn't exist.
Wipes any leftover tables in the db file.
"""

from .database import engine
import sqlalchemy as sa

def initial_setup():

    # Using a direct SQL for now as it's easier.
    # Maybe later could update to use models.py module and create the ORM models.

    with engine.connect() as conn:
        # 1. Get all table names
        result = conn.execute(
            sa.text("SELECT name FROM sqlite_master WHERE type='table';")
        )
        tables = [row[0] for row in result]

        # 2. Drop each table and run VACUUM to make sure the file size decreases
        for table in tables:
            conn.execute(sa.text(f'DROP TABLE IF EXISTS "{table}"'))
            conn.execute(sa.text("VACUUM"))

    print("Database (re-)created at:", engine.url, "...")
    print("Initial Setup Completed.")