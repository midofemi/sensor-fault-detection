
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from main import set_env_variable
import os

if __name__=='__main__':
    data_file_path="C:/Users/midof/OneDrive/Desktop/INeuron/Data_Science_Project/Industry_Ready_Proj/sensor-fault-detection-GIT/aps_failure_training_set1.csv"
    env_file_path="C:/Users/midof/OneDrive/Desktop/INeuron/Data_Science_Project/Industry_Ready_Proj/Sensor_Detection_Project/env.yaml"
    set_env_variable(env_file_path)
    print(os.environ['MONGO_DB_URL'])
    sd = SensorData()
    if DATA_INGESTION_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[DATA_INGESTION_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=data_file_path,collection_name=DATA_INGESTION_COLLECTION_NAME)