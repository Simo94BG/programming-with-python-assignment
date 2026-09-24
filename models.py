from sqlalchemy import Column, Integer, Float
from database import Base

def create_model(tablename: str, columns: dict):

    # Main attributes of table
    main_attrs = {
        "__tablename__": tablename, # Table name
        "id": Column(Integer, primary_key=True) # ID as int
    }

    main_attrs.update(columns) # Add extra columns
    return type(tablename.capitalize(), (Base,), main_attrs)

RawIdeal = create_model(
    "raw_ideal",
    {
        "x": Column(Float)
        ,**{f"y{i}": Column(Float) for i in range(1, 51)} # Shortened down to 1 line with the help of Copilot
    }
)

RawTrain = create_model(
    "raw_train",
    {
        "x":Column(Float)
        ,**{f"y{i}": Column(Float) for i in range(1, 5)}
    }
)

RawTest = create_model(
    "raw_test",
    {
        "x": Column(Float)
        ,"y": Column(Float)
    }
)