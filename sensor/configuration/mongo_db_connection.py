
import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import certifi
import os
from sensor.logger import logging

ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                #mongo_db_url = MONGODB_URL_KEY
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                print(mongo_db_url)
                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url) 
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"[MONGODB] Connected to database: {database_name}")
            logging.info(f"[MONGODB] Collections: {self.database.list_collection_names()}")
        except Exception as e:
            raise e
        
