from abc import ABC, abstractmethod
import numpy as np


class AbstractImageFileProcessor(ABC):
    def __init__(self, file_path: str):
        self._file_path = file_path

    @abstractmethod
    def _load_all_data(self) -> None:
        # Can be overridden to load data in a different format.
        pass

    @property
    @abstractmethod
    def cleaned_data(self) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def loaded_data(self) -> np.ndarray:
        pass


class CsvImageFileProcessor(AbstractImageFileProcessor):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        try:
            self._load_all_data()
        except Exception as e:
            raise Exception(f"Error loading data from {file_path}: {e}")

    def _load_all_data(self) -> None:
        # Load data and remove rows containing NaN values
        self._loaded_data = np.genfromtxt(self._file_path, delimiter=",")

    @property
    def cleaned_data(self) -> np.ndarray:
        return self._loaded_data[~np.isnan(self._loaded_data).any(axis=1)].astype(
            np.float32
        )  # Remove rows containing NaN values. In the given data, NaN values are present in the last row and first row(column names).

    @property
    def loaded_data(self) -> np.ndarray:
        return self._loaded_data
