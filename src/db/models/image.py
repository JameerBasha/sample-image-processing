from typing import Optional

from sqlmodel import Field, SQLModel

from src.services.image_processing.processor import ResizeInterpolationMode


class ImageData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    file_name: Optional[str] = Field(default=None)
    width: int
    height: int
    data: bytes  # This is efficient because postgres supports streaming bytes data which can be used if data set is large. Also using bytes we can convert directly to numpy array which removes the overhead which comes with python native objects.


# class ImageData(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     image_meta_data_id: int = Field(foreign_key="imagemetadata.id")
#     column_depth: float
#     row_data: list[int] = Field(sa_type=ARRAY(Integer)) # By storing each row separately, we can filter the rows based on the column depth. But this is not efficient due to the overhead of python native objects.
