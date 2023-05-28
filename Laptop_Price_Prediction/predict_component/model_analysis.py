import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from Laptop_Price_Prediction import predict_utils
import sys
import os
from Laptop_Price_Prediction.predict_entity import predict_artifact_config
from lazypredict.Supervised import LazyRegressor
import optuna
import pickle
from Laptop_Price_Prediction.models import Model_main
from autogluon.tabular import TabularPredictor
from sklearn.metrics import r2_score

class ModelAnalysis:
    
    def __init__(self,DataSepration_artifact,Model_Analysis_config):
        self.DataSepration_artifact = DataSepration_artifact
        self.Model_Analysis_config = Model_Analysis_config
      

    
    def initiate_model_analysis(self):
        X_train = np.load(self.DataSepration_artifact.feature_store_x_train)
        X_test = np.load(self.DataSepration_artifact.feature_store_x_test)
        y_train =np.load( self.DataSepration_artifact.feature_store_y_train)
        y_test = np.load(self.DataSepration_artifact.feature_store_y_test)
        columns = ['Brand Name', 'Processor', 'RAM',"Storage","os"]
        columns_y=['Prices']
        X_train=pd.DataFrame(X_train,columns=columns)
        X_test=pd.DataFrame(X_test,columns=columns)
        y_train=pd.DataFrame(y_train,columns=columns_y)
        y_test=pd.DataFrame(y_test,columns=columns_y)
        # Concatenate x_train and y_train as columns
        concatenated_data = pd.concat([X_train, y_train], axis=1)

        # Create and fit the AutoML predictor
        predictor = TabularPredictor(label='Prices', eval_metric='r2',verbosity=1).fit(concatenated_data,)
       
        # Get the best model
        best_model = predictor.get_model_best()
      

        # Print the best model
        print("Best model:", best_model)
        predictions = predictor.predict(X_test)
        r2 = r2_score(y_test, predictions)
        print("R-squared:", r2)
        os.makedirs(self.Model_Analysis_config.FinalModelFolder , exist_ok=True)
        # save the model to disk
        logging.info("Sttoring the model Object")
        pickle.dump(predictions, open(self.Model_Analysis_config.FinalModel, 'wb'))
        model_artifact =predict_artifact_config.DataModelArtifact(final_models=self.Model_Analysis_config.FinalModel)
        
        return model_artifact
        # os.makedirs(self.Model_Analysis_config.ModelAnalysisFolder,exist_ok=True)
        # logging.info("Starting model analysis")
        # print("\n working on model analyis running Lazy regressor")
        # clf = LazyRegressor(verbose=0,ignore_warnings=True, custom_metric=None)
        # models,predictions = clf.fit(X_train, X_test, y_train, y_test)
        # print("Lazy regressor ended")
        # print(models)
        # model_top_ = models[models['R-Squared']>0.70]

        # model_name_top=model_top_.index.tolist()
    
        

        # print(model_name_top)
        # models = models[models['R-Squared']>0.00]
        # models=models[['Adjusted R-Squared']]
        

        # models.to_csv(self.Model_Analysis_config.ModelAnalysisfile, sep='\t')
        # Model_main_data=Model_main.Model_main(self.DataSepration_artifact,model_name_top)
        # all_models=Model_main_data.intiate_models()

        # file1 = open(self.Model_Analysis_config.ModelAnalysisfile, "a")
        # for key,value in all_models.items():

        #     file1.writelines("--------------------------------------- "+key+" ------------------------------------- \n")
        #     file1.writelines("Model Name "+value["Model Name"]+"\n")
        #     file1.writelines("Hyper parameters "+str(value["Hyper parameters"])+"\n")
        #     file1.writelines("Accurcy of the models "+str(value['Model_score']*100)+"% \n")
         
        #     file1.writelines("###################################################################################### \n \n")
        # max_score=-1
        # max_data={}
        # for key,value in all_models.items():
        #     if max_score<value['Model_score']:
        #         max_data=value
        #         max_score=value['Model_score']
        # logging.info("Ending Model analysis")
        # logging.info("Creating a Model file")
        
      
        # os.makedirs(self.Model_Analysis_config.FinalModelFolder , exist_ok=True)
        # # save the model to disk
        # logging.info("Sttoring the model Object")
        # pickle.dump(max_data['Model_Object'], open(self.Model_Analysis_config.FinalModel, 'wb'))
        # model_artifact =predict_artifact_config.DataModelArtifact(final_models=self.Model_Analysis_config.FinalModel)
        
        # return model_artifact