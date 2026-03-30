from pydantic import BaseModel

class ObservationSchema(BaseModel):
    id: int
    data: str

    class Config:
        from_attributes = True # To read data from SQLAlchemy objects
