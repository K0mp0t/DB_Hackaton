from typing import Callable, Optional, Text
import joblib


class ModelLoader:
    """
    Loading a machine learning model from a file and providing
    access to it through the get_model method.
    Singleton
    """
    _instance: Optional[object] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.model_path: Text = '../models/all_comp_model.pkl'
        self._load_model()

    def get_model(self) -> Callable:
        if not self.model:
            self._load_model()

        return self.model

    def _load_model(self) -> None:
        self.model: Optional[Callable] = joblib.load(self.model_path)


class ROFLDatabase:
    """
    Class that acts like a database. Singleton
    """

    _instance: Optional[object] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # TODO: db_init
        # smth: self.storage = {"predicts":
        #     {"date": [], "data": [], "predictions": [], "is_error": []}}
        pass

    def read(self, task: Callable) -> None:
        # TODO: db_read
        raise NotImplementedError('fastapi.utils db_read not implemented')

    def write(self, task: Callable) -> None:
        # TODO: db_read
        raise NotImplementedError('fastapi.write db_read not implemented')
