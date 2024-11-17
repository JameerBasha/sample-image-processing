
from sqlalchemy.orm import Session

from src.db.models.image import ImageData


class ImageDBService:
    def __init__(self, db: Session):
        self.db = db

    def write_image_to_db(
        self, image_bytes: bytes, file_name: str, width: int, height: int
    ):
        """Store image data in the database"""
        image_data = ImageData(
            file_name=file_name, width=width, height=height, data=image_bytes
        )
        self.db.add(image_data)
        self.db.commit()

    def get_image_data_from_db(self, image_data_id: int) -> ImageData:
        """Retrieve images from database based on id"""
        img = self.db.query(ImageData).filter(ImageData.id == image_data_id).first()
        if not img:
            raise ValueError(f"Image with id {image_data_id} not found")
        return img
