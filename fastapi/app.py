from typing import Callable

import pandas as pd
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    Response
)
from pydantic import BaseModel

from src.predictions import get_predictions, save_predictions
from utils import ModelLoader

import json

app = FastAPI()
model_loader: ModelLoader = ModelLoader()


class Features(BaseModel):
    start: int
    stop: int


@app.get('/')
def index() -> HTMLResponse:
    return HTMLResponse('<h1><i>API ON AIR. AI Talent Hub</i></h1>')


@app.post('/predict')
def predict(
        response: Response,
        interval: Features,
        background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Handle POST requests to '/predict' endpoint.
    Parameters:
        response (Response): The response object.
        interval (Features): The interval object containing start and stop values.
        background_tasks (BackgroundTasks): The background tasks object.
    Returns:
        JSONResponse: The JSON response containing the predictions and real values.
    Raises:
        Exception: If an error occurs during the prediction process.
    Notes:
        - The 'read_json' function may be deprecated.
        - The 'model_loader' module is used to load the model.
        - The 'get_predictions' function is called to generate predictions.
        - The 'save_predictions' function is called to save predictions in the background.
        - If an exception occurs, a 500 status code is set and the error message is returned.
    """
    try:
        # hint: read_json may be deprecated
        model: Callable = model_loader.get_model()
        predictions, real = get_predictions(model, interval.start, interval.stop)
        background_tasks.add_task(save_predictions, interval)
        return JSONResponse(content={'predictions': json.dumps(list(predictions)), 'real': json.dumps(list(real))})
    except Exception as e:
        response.status_code = 500
        # TODO: loguru logger here
        return JSONResponse(content={'error_bruh': str(e)})


@app.get('/evaluate')
def evaluate() -> JSONResponse:
    # Сюда-то можно и сделать eval!
    raise NotImplementedError('src/evaluate not implemented do smth about it (or dont)')


@app.get('/anomalies')
def anomalies(
        response: Response,
        interval: Features,
) -> JSONResponse:
    """
    Handle GET requests to '/anomalies' endpoint.
    Parameters:
        response (Response): The response object.
        interval (Features): The interval object containing start and stop values.
    Returns:
        JSONResponse: The JSON response containing the lsit of anomalies.
    Raises:
        Exception: If an error occurs during the prediction process.
    """
    try:
        raise NotImplementedError('src/anomalies not implemented do smth about it (or dont)')
    except Exception as e:
        response.status_code = 500
        # TODO: loguru logger here
        return JSONResponse(content={'error_bruh': str(e)})


if __name__ == "__main__":
    # Run the server
    # see: http://%host%:5000/docs# for more information
    # change host to 0.0.0.0 if need
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
