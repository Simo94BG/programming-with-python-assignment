"""
Database module enabling the use of sqlalchemy to store datasets in the database.
"""

from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///data/datasets.db"
engine = create_engine(DATABASE_URL, echo=False)