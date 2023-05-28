import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from sklearn.preprocessing import StandardScaler
from Laptop_Price_Prediction import predict_utils
import sys
import os
from Laptop_Price_Prediction.predict_entity import predict_artifact_config

import pickle

class DataSepration:
    def __init__(self,data_pre_processor_artifact,DataSeprationConfig):
        try:
            self.data_pre_processor_artifact = data_pre_processor_artifact
            self.DataSeprationConfig = DataSeprationConfig
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

    def initiate_data_sepration(self):
        try:
            logging.info("Seprate x and y data")
            df=pd.read_csv(self.data_pre_processor_artifact.feature_store_file_path_data)
            
            x=df.drop("prices",axis=1)
            y=df["prices"]
            logging.info("Scaling the values")
            scaler = StandardScaler()
            x = scaler.fit_transform(x)
            y=np.log(y)
            pickle.dump(scaler, open(self.DataSeprationConfig.scalar_pickle, 'wb'))

            logging.info("Spliting the data into 80-20")
            X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=.20,random_state =123)
            os.makedirs(self.DataSeprationConfig.DataSeprationFolder,exist_ok=True)
            os.makedirs(self.DataSeprationConfig.TrainingFolder,exist_ok=True)
            os.makedirs(self.DataSeprationConfig.TestingFolder,exist_ok=True)
            np.save(self.DataSeprationConfig.x_TrainFile,X_train)
            np.save(self.DataSeprationConfig.y_TrainFile,y_train)
            np.save(self.DataSeprationConfig.x_TestFile,X_test)
            np.save(self.DataSeprationConfig.y_TestFile,y_test)
            
            DataSepration_artifact = predict_artifact_config.DataSeprationArtifact(feature_store_x_train=self.DataSeprationConfig.x_TrainFile
                                                                                   ,feature_store_x_test=self.DataSeprationConfig.x_TestFile
                                                                                   ,feature_store_y_test=self.DataSeprationConfig.y_TestFile
                                                                                   ,feature_store_y_train=self.DataSeprationConfig.y_TrainFile
                                                                                   ,scalar_pickle=self.DataSeprationConfig.scalar_pickle
                                                                                   )
            return DataSepration_artifact


        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

    