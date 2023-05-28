import optuna
import numpy as np
import pandas as pd
from Laptop_Price_Prediction.predict_entity import predict_artifact_config
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
# from Laptop_Price_Prediction.models import models_space
import inspect
from Laptop_Price_Prediction.models import models_space
from sklearn.model_selection import GridSearchCV


class Model_main:
    def __init__(self,predict_artifact_config,model_name_top) :
        self.predict_artifact_config = predict_artifact_config
        self.model_name_top = model_name_top
        
    
    def intiate_models(self):
        all_models={}
        models=models_space.model_space()
        X_train = np.load(self.predict_artifact_config.feature_store_x_train)
        y_train =np.load( self.predict_artifact_config.feature_store_y_train)
        X_test = np.load(self.predict_artifact_config.feature_store_x_test)
        y_test = np.load(self.predict_artifact_config.feature_store_y_test)
        for model_name, model_info in models.items():
        
            model_data={}
            model = model_info['model']
            params = model_info['params']
            grid_search = GridSearchCV(model, params, cv=5)
            grid_search.fit(X_train, y_train)
            model_data["Model Name"]=model_name
            model_data["Hyper parameters"]= grid_search.best_params_
            
            model.set_params(**model_data["Hyper parameters"])
            model.fit(X_test, y_test)
            model_data['Model_Object']=model
            

            model_data["Model_score"]=model.score(X_train,y_train)
          
            all_models[model_name]=model_data
            
        return all_models


        
                