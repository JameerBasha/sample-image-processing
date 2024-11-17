import logging
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session

from src.db.database import get_db
from src.services.image_db_service import ImageDBService
from src.services.image_processing.constants import CUSTOM_COLOR_MAP
from src.services.image_processing.image_converter import JpegImageConverter
from src.services.image_processing.processor import ImageProcessor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{image_data_id}", response_class=Response)
async def get_image(
    image_data_id: int,
    depth_min: Optional[float] = Query(None, description="Minimum column depth filter"),
    depth_max: Optional[float] = Query(None, description="Maximum column depth filter"),
    db: Session = Depends(get_db),
):
    start_time = time.time()
    try:
        image_data = ImageDBService(db).get_image_data_from_db(image_data_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        filtered_image_frame = ImageProcessor(
            image_data=image_data.data,
            height=image_data.height,
            width=image_data.width,
            image_converter=JpegImageConverter,
        ).get_filtered_image_frame(depth_min, depth_max, CUSTOM_COLOR_MAP)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    end_time = time.time()
    logger.info(
        f"Time taken to process image {image_data_id} min {depth_min} max {depth_max} color_map {CUSTOM_COLOR_MAP}: {end_time - start_time} seconds"
    )
    return Response(
        content=filtered_image_frame, media_type=JpegImageConverter.media_type
    )
