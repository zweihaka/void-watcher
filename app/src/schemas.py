from pydantic import BaseModel

class ObservationSchema(BaseModel):
    id: int
    mass: str

    class Config:
        from_attributes = True # To read data from SQLAlchemy objects
