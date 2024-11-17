import enum
from matplotlib.colors import LinearSegmentedColormap


class ResizeInterpolationMode(enum.Enum):
    # Higher the value, higher the quality but slower the processing.
    NEAREST = 0
    LINEAR = 1
    QUADRATIC = 2
    CUBIC = 3
    QUARTIC = 4
    QUINTIC = 5


CUSTOM_COLOR_MAP = LinearSegmentedColormap.from_list(
    "custom", ["blue", "red", "yellow", "gray", "black"]
)
