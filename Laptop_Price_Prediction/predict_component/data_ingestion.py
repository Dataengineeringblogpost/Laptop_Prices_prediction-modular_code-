import pandas as pd
import numpy as np
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
import sys
import os
from Laptop_Price_Prediction.predict_entity import predict_artifact_config




class DataIngestion:
    def __init__(self,data_ingestion_config):
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

    """
    Objective:- 
    1)Here we are converting the data to a dataframe then removing the duplicate rows
    2)Replacing empty cell with NaN
    3)Droping the index columns
    """
    def intitate_data_ingestion(self):
        try:
            
            logging.info("Dataframe created")
            data_file_path = self.data_ingestion_config.data_file_path
            print(data_file_path)

            df=pd.read_excel(data_file_path)


            #replace space with nan
            df=df.replace(" ",np.NAN)
            df=df.replace("na",np.NaN)
            df=df.replace("nan",np.NaN)
            
            #Droping the unneccsary column and dropping duplicates
            df.drop("Unnamed: 0",inplace=True,axis=1)
            df.drop_duplicates(inplace=True)
            #Shape of the data
            
            data_ingestion_artifact_path = self.data_ingestion_config.artifact_file_path+"\\Data_Ingestion"
            data_ingestion_artifact_datasets_path=self.data_ingestion_config.artifact_file_path+"\\Data_Ingestion\\Datasets"
            dataset_file_path = data_ingestion_artifact_datasets_path+"\\dataset.csv"

            os.makedirs(data_ingestion_artifact_path,exist_ok=True)
            os.makedirs(data_ingestion_artifact_datasets_path,exist_ok=True)
            df.to_csv(path_or_buf=dataset_file_path,index=False,header=True)
            data_ingestion_artifact=predict_artifact_config.DataIngestionArtifact(feature_store_file_path=dataset_file_path)
            return data_ingestion_artifact



        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)