from database import engine
import sqlalchemy as sa

with engine.connect() as conn:
    conn.execute(sa.text("DROP TABLE IF EXISTS raw_test"))