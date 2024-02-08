import os
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
import logging

class CosmosDB():
    def __init__(self):
        # Cosmos DB connection information
        self.endpoint = os.environ["endpoint"]
        self.key = os.environ["key"]
        self.database_id = "ml-data"
        self.container_id = "robot"
        self.partition_key = "/id"
        self.client = CosmosClient(self.endpoint, self.key)

    def create(self, data):
        # Create or get a reference to a database
        try:
            database = self.client.create_database_if_not_exists(id=self.database_id)
            logging.info(f'Database "{self.database_id}" created or retrieved successfully.')

        except exceptions.CosmosResourceExistsError:
            database = self.client.get_database_client(self.database_id)
            logging.info('Database with id \'{0}\' was found'.format(self.database_id))

        # Create or get a reference to a container
        try:
            container = database.create_container(id=self.container_id, partition_key=PartitionKey(path='/partitionKey'))
            logging.info('Container with id \'{0}\' created'.format(self.container_id))

        except exceptions.CosmosResourceExistsError:
            container = database.get_container_client(self.container_id)
            logging.info('Container with id \'{0}\' was found'.format(self.container_id))

        # Create item in database
        try :
            container.create_item(body=data)
        except exceptions.CosmosResourceExistsError:
            logging.info('Record aready exists in database. Please modify your request')