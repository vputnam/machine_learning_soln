import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
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

    # Cosmos DB connection information
    endpoint = os.environ["endpoint"]
    key = os.environ["key"]
    database_id = "ml-data"
    container_id = "robot"
    partition_key = "/id"

    # Set the total throughput (RU/s) for the database and container
    database_throughput = 2000

    # Initialize the Cosmos client
    client = CosmosClient(endpoint, key)

    # Create or get a reference to a database
    try:
        database = client.create_database_if_not_exists(id=database_id)
        logging.info(f'Database "{database_id}" created or retrieved successfully.')

    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_id)
        logging.info('Database with id \'{0}\' was found'.format(database_id))

    # Create or get a reference to a container
    try:
        container = database.create_container(id=container_id, partition_key=PartitionKey(path='/partitionKey'))
        logging.info('Container with id \'{0}\' created'.format(container_id))

    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_id)
        logging.info('Container with id \'{0}\' was found'.format(container_id))

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
        person = data_models.DBData(**data)
    except ValidationError:
        logging.info('Database record malformed. Check structure.')
        return func.HttpResponse(
            "Database record malformed. Please see documentation for proper shape.",
            status_code=400
        )

    # Create item in database
    try :
        container.create_item(body=data)
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

