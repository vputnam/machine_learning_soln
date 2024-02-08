import azure.functions as func
import logging
import numpy as np
import pandas as pd
import pickle
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="Predict")
def Predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()

    try :
        loaded_model = pickle.load(open('RandomForestRegressor.pkl', 'rb'))
    except FileNotFoundError:
        raise Exception("Model file not found.")

    try:
        X_test = req_body.get('X_test')
    except ValueError:
        raise Exception("Please include X_test parameter values in body.")
    else:
        data = pd.json_normalize(X_test)
        prediction = loaded_model.predict(data)
        prediction_json = json.dumps({'prediction': prediction.tolist()})

    return func.HttpResponse(
            prediction_json,
            status_code=200
    )