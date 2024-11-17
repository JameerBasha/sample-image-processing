import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from skimage import transform

from src.services.image_processing.constants import ResizeInterpolationMode
from src.services.image_processing.file_processors import (
    AbstractImageFileProcessor,
    CsvImageFileProcessor,
)
from src.services.image_processing.image_converter import (
    AbstractImageConverter,
    JpegImageConverter,
)


class ImageProcessor:
    def __init__(
        self,
        image_data: bytes = None,
        height: int = None,
        width: int = None,
        file_path: str = "",
        file_processor: AbstractImageFileProcessor = CsvImageFileProcessor,
        image_converter: AbstractImageConverter = JpegImageConverter,
    ):
        self._file_path = file_path
        if not image_data:
            self._raw_data = file_processor(self._file_path).cleaned_data
        else:
            # Calculate dimensions from bytes
            total_float_count = len(image_data) // 4  # since float32 is 4 bytes
            calculated_height = total_float_count // (width + 1)  # +1 for depth column

            self._raw_data = np.frombuffer(image_data, dtype=np.float32).reshape(
                calculated_height, width + 1
            )
        self._image_converter = image_converter

    def resize_image(
        self, width: int, mode: ResizeInterpolationMode = ResizeInterpolationMode.LINEAR
    ) -> None:
        # Height resizing is not supported because column depth value is lost during resizing.
        # Resize the image and add the column depths to the resized image and update the raw data.
        self._raw_data = np.column_stack(
            (
                self.column_depths,
                transform.resize(
                    self.image_data,
                    (self.height, width),
                    order=mode.value,  # Interpolation mode
                    preserve_range=True,  # This is required to preserve the range of the pixel values from the original image.
                ),
            )
        )

    @property
    def bytes_data(self) -> np.ndarray:
        return self._raw_data.tobytes()

    @property
    def width(self) -> int:
        return self.image_data.shape[1]

    @property
    def height(self) -> int:
        return self.image_data.shape[0]

    @property
    def image_data(self) -> np.ndarray:
        return self._raw_data[:, 1:]

    def get_image_data_for_resizing(self) -> np.ndarray:
        return self._raw_data[:, 1:].astype(
            np.uint8
        )  # Convert the image data to uint8 to preserve the range of the pixel values from the original image.

    @property
    def column_depths(self) -> list[float]:
        return self._raw_data[:, 0]

    @property
    def file_name(self) -> str:
        return self._file_path.split("/")[-1]

    def get_filtered_image_data(
        self, depth_min: float = None, depth_max: float = None
    ) -> np.ndarray:
        # Create mask for rows where depth is within range
        depth_mask = []
        if depth_min is not None:
            depth_mask.append(self._raw_data[:, 0] >= depth_min)
        if depth_max is not None:
            depth_mask.append(self._raw_data[:, 0] <= depth_max)

        if not depth_mask:
            # If no filters applied, return all image data
            return self._raw_data[:, 1:].astype(np.uint8)

        depth_mask = np.all(depth_mask, axis=0)

        # Apply mask and return only the image data columns (excluding depth column)
        return self._raw_data[depth_mask][:, 1:].astype(np.uint8)

    def get_filtered_image_frame(
        self,
        depth_min: float,
        depth_max: float,
        color_map: LinearSegmentedColormap = None,
    ) -> bytes:
        filtered_image_data = self.get_filtered_image_data(depth_min, depth_max)
        if not filtered_image_data.size:
            raise ValueError("No image data found after applying filters")
        return self._image_converter.get_image_bytes(
            filtered_image_data, color_map=color_map
        )

    def get_image_frame(self, color_map: str = None) -> bytes:
        return self._image_converter.get_image_bytes(
            self.image_data, color_map=color_map
        )
