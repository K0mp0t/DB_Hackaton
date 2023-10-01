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
    Endpoint for making predictions.
    This function receives a POST request with a features_item, reads the features batch,
    computes predictions using a model, and saves the predictions to a *rofl* database in the background.
    Finally, it returns a JSON response with the predictions serialized as a JSON string.
    Parameters:
    - response (Response): The response object for setting the status code in case of an exception.
    - features_item (Features): The features item received in the POST request.
    - background_tasks (BackgroundTasks): The background tasks object for adding the task to save predictions
    to the database.
    Returns:
    - JSONResponse: The JSON response containing the predictions serialized as a JSON string.
    Raises:
    - Exception: If any error occurs during the prediction process, an exception is raised and a JSON response with the
    error message is returned.
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


if __name__ == "__main__":
    # Run the server
    # hint: see http://%host%:5000/docs# for more information
    # change host to 0.0.0.0 if need
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
