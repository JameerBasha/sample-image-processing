import io
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image


class AbstractImageConverter(ABC):

    media_type: str

    @abstractmethod
    def get_image_bytes(
        self, image_data: np.ndarray, quality: int = 95, color_map: str = None
    ) -> bytes:
        pass


class JpegImageConverter(AbstractImageConverter):

    media_type = "image/jpeg"

    @staticmethod
    def get_image_bytes(
        image_data: np.ndarray,
        quality: int = 100,
        color_map: LinearSegmentedColormap = None,
    ) -> bytes:
        """
        Convert numpy array image data to JPG bytes with optional colormap.
        """
        if color_map:
            cmap = plt.get_cmap(color_map)
            image_data = cmap(image_data)
            image_data = (image_data * 255).astype(np.uint8)
        image = Image.fromarray(image_data.astype(np.uint8))
        buffer = io.BytesIO()
        if image.mode == "RGBA":
            image = image.convert(
                "RGB"
            )  # when applying colormap, image mode is changed to RGBA.
        image.save(buffer, format="JPEG", quality=quality)
        return buffer.getvalue()
