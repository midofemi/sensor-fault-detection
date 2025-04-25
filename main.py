from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, File, UploadFile, Request
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):
    if os.getenv('MONGO_DB_URL',None) is None: 
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
@app.post("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        #get data from user csv file
        df = pd.read_csv(file.file)
        # Replace "na" with NaN
        df.replace({"na": np.nan}, inplace=True)

        # Define columns to remove
        columns_to_remove = ['br_000', 'bq_000', 'bp_000', 'ab_000', 'cr_000', 'bo_000', 'bn_000']

        # Drop the specified columns
        df = df.drop(columns=columns_to_remove)

        # Initialize the preprocessing transformers
        robust_scaler = RobustScaler()
        simple_imputer = SimpleImputer(strategy="constant", fill_value=0)

        # Create a pipeline for preprocessing
        preprocessor = Pipeline(
            steps=[
                ("Imputer", simple_imputer),
                ("RobustScaler", robust_scaler)
            ]
        )

        # Fit and transform the data with the preprocessor
        df_processed = preprocessor.fit_transform(df)

        # Convert the NumPy array back to a DataFrame with column names
        df = pd.DataFrame(df_processed, columns=df.columns)
        #print(df)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        df.to_csv("C:/Users/midof/OneDrive/Documents/Dataset/aps_failure123455555555555.csv")
        return df.to_html()
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")
   
if __name__ == '__main__':
    app_run(app, host=APP_HOST, port=APP_PORT)


#To run Main.py with the app
#- uvicorn main:app
