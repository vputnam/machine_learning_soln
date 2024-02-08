import azure.functions as func
from azure.cosmos import exceptions
import cosmos_db
import json
import logging
import data_models
import os
import pandas as pd
import pickle
from pydantic import BaseModel, ValidationError

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="Create")
def Create(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check for data in request body 
    try:
        req_body = req.get_json()
        data = req_body.get('data')
    except ValueError:
        logging.info('X_test data not included in request body. Please modify your request and try again.')
        return func.HttpResponse(
            "Data not included in request body. Please modify your request and try again.",
            status_code=400
        )
    
    # Validate JSON body shape 
    try: 
        validate = data_models.DBData(**data)
    except ValidationError:
        logging.info('Database record malformed. Check structure.')
        return func.HttpResponse(
            "Database record malformed. Please see documentation for proper shape.",
            status_code=400
        )

    # Create item in database
    try :
        cosmosClient = cosmos_db.CosmosDB()
        cosmosClient.create(data)
    except exceptions.CosmosResourceExistsError:
        logging.info('Record aready exists in database. Please modify your request')
        return func.HttpResponse(
            "Record aready exists in database. Please modify your request",
            status_code=400
        ) 

    return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
    )

@app.route(route="Predict")
def Predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    

    try :
        loaded_model = pickle.load(open('model.pkl', 'rb'))
    except FileNotFoundError:
        raise Exception("Model file not found.")

    
    # Check for X test in request body 
    try:
        req_body = req.get_json()
        X_test = req_body.get('X_test')
    except ValueError:
        logging.info('X_test data not included in request body. Please modify your request and try again.')
        return func.HttpResponse(
            "X_test data not included in request body. Please modify your request and try again.",
            status_code=400
        )

    # Validate JSON body shape 
    try:
        for record in X_test: 
            validate = data_models.TestDataX(**record)
    except ValidationError:
        logging.info('At least one X_test record malformed. Check structure.')
        return func.HttpResponse(
            "X_test record malformed. Please see documentation for proper shape.",
            status_code=400
        )        

    data = pd.json_normalize(X_test)
    prediction = loaded_model.predict(data)
    prediction_json = json.dumps({'prediction': prediction.tolist()})

    return func.HttpResponse(
            prediction_json,
            status_code=200
    )

