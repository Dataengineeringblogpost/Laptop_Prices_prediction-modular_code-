import os
import sys
from datetime import datetime
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging


class PredictPipelineConfig:
    def __init__(self,data_file_path) -> None:
        try:
            self.data_file_path = data_file_path
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        
class DataIngestionConfig:
    def __init__(self,PredictPipelineConfig) :
        try:
            self.data_file_path = PredictPipelineConfig.data_file_path
            self.artifact_file_path = os.path.dirname(PredictPipelineConfig.data_file_path)
            

        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

class DataTransformationConfig:
    def __init__(self,DataIngestionConfig):
        try:
            self.data_file_path = DataIngestionConfig.data_file_path
            self.artifact_file_path = DataIngestionConfig.artifact_file_path
            self.artifact_folder_path_DataTransformation = self.artifact_file_path+"\\Data_Transformation"
            self.artifact_database_folder_path_DataTransformation = self.artifact_folder_path_DataTransformation +"\\Datasets"
            self.artifact_database_file_path_DataTransformation = self.artifact_database_folder_path_DataTransformation+"\\Data_Transformation_dataset.csv"
            
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)     
        
class DataPreProcessConfig:
    def __init__(self,DataTransformationConfig) :
        try:
            
            self.artifact_file_path = DataTransformationConfig.artifact_file_path
            self.convert_json_file = self.artifact_file_path + "\\convert_json.json"
            self.artifact_file_path_processing_main = self.artifact_file_path + "\\Data_Pre_Processing"
            self.artifact_file_path_processing_main_dataset = self.artifact_file_path_processing_main+"\\Dataset"
            self.artifact_file_path_processing_main_dataset_null = self.artifact_file_path_processing_main+"\\Dataset_null"
            self.artifact_file_path_processing_main_dataset_data = self.artifact_file_path_processing_main_dataset+"\\Data_PreProcessing_dataset.csv"
            self.artifact_file_path_processing_main_dataset_null_data = self.artifact_file_path_processing_main_dataset_null+"\\Data_PreProcessing_dataset_null.csv"
            self.artifact_file_path_processing_main_dataset_data_1 = self.artifact_file_path_processing_main_dataset+"\\Data_PreProcessing_dataset_1.csv"
            self.artifact_file_path_processing_main_dataset_null_data_1 = self.artifact_file_path_processing_main_dataset_null+"\\Data_PreProcessing_dataset_null_1.csv"

        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

class DataSeprationConfig:
    def __init__(self,DataPreProcessConfig):
        try:
            self.artifact_file_path = DataPreProcessConfig.artifact_file_path
            self.DataSeprationFolder = DataPreProcessConfig.artifact_file_path + "\\DataSepration"
            self.TrainingFolder = self.DataSeprationFolder + "\\Training"
            self.TestingFolder = self.DataSeprationFolder+ "\\Testing"
            self.x_TrainFile = self.TrainingFolder +"\\X_train.npy"
            self.y_TrainFile = self.TrainingFolder +"\\Y_train.npy"
            self.x_TestFile = self.TestingFolder +"\\X_test.npy"
            self.y_TestFile = self.TestingFolder +"\\Y_test.npy"
            self.scalar_pickle = self.artifact_file_path + "\\Scalar.pkl"
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        
class ModelAnalysisConfig:
    def __init__(self,DataSeprationConfig):
        try:
            self.artifact_file_path=DataSeprationConfig.artifact_file_path
            self.ModelAnalysisFolder =self.artifact_file_path + "\\ModelAnalysis"
            self.ModelAnalysisfile = self.ModelAnalysisFolder +"\\ModelAnalysis.txt"
            self.FinalModelFolder = self.artifact_file_path + "\\FinalModels"
            self.FinalModel = self.FinalModelFolder + "\\FinalModel.pkl"
            

        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
