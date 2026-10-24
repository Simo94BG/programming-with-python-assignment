from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///data/written_assignment.db"
engine = create_engine(DATABASE_URL, echo=False)