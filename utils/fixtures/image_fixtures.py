import logging

from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.image_db_service import ImageDBService
from src.services.image_processing.file_processors import CsvImageFileProcessor
from src.services.image_processing.processor import (ImageProcessor,
                                                     ResizeInterpolationMode)

logger = logging.getLogger(__name__)


def load_sample_image_data_to_db(db: Session = None):
    if not db:
        db = next(get_db())
    image_processor = ImageProcessor(
        file_path="sample_data/img.csv", file_processor=CsvImageFileProcessor
    )
    image_processor.resize_image(width=150, mode=ResizeInterpolationMode.NEAREST)
    ImageDBService(db).write_image_to_db(
        image_bytes=image_processor.bytes_data,
        file_name=image_processor.file_name,
        width=image_processor.width,
        height=image_processor.height,
    )
    logger.info("Sample image data loaded to db")


if __name__ == "__main__":
    load_sample_image_data_to_db()
