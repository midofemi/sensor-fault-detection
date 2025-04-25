import sys
from typing import Optional

import numpy as np
import pandas as pd
import json
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException

from sensor.logger import logging



class SensorData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise SensorException(e, sys)


    def save_csv_file(self,file_path ,collection_name: str, database_name: Optional[str] = None):
        try:
            data_frame=pd.read_csv(file_path)
            print(data_frame)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise SensorException(e, sys)


    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            logging.info(f"[EXPORT] Attempting to access MongoDB collection '{collection_name}'")
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            #First, retrieve the documents from MongoDB
            documents = list(collection.find())
            logging.info(f"[EXPORT] Retrieved {len(documents)} documents from collection '{collection_name}'")

            if not documents:
                logging.warning(f"[EXPORT] No documents found in collection '{collection_name}'")
                return pd.DataFrame()
            #df = pd.DataFrame(list(collection.find()))
            df = pd.DataFrame(documents)
            if "_id" in df.columns.to_list(): 
                df = df.drop(columns=["_id"], axis=1) 
            df.replace({"na": np.nan}, inplace=True) 
            return df
        except Exception as e:
            raise SensorException(e, sys)