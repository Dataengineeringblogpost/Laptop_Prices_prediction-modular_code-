import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from Laptop_Price_Prediction import predict_utils
import sys
import os
from Laptop_Price_Prediction.predict_entity import predict_artifact_config
import json
class DataPreProcessing:
    def __init__(self,data_transformation_artifact,data_pre_processing_config) :
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.data_pre_processing_config = data_pre_processing_config

        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
    
    def intitate_data_pre_processing(self):
        try:
            logging.info("Calling the pre-processing .csv file and Creating a Dataframe ")
            df=pd.read_csv(self.data_transformation_artifact.feature_store_file_path)
            logging.info("Naming the columns")
            df = df[['brand_name','processor_brand',"2","3","4","5"]]
            df.columns=['brand_name','processor_brand',"ram","os","storage","prices"]
            logging.info("Deleting the rows with count less than 5")
            col=['brand_name','processor_brand',"ram","os","storage"]
            # for col_name in col:
            #     predict_utils.del_rows_count(df,col_name) 

            logging.info("Data information")
            shape_data = df.shape
            
            logging.info(" Row :- "+str(shape_data[0])+", Columns:- "+str(shape_data[1]))
            missing_percentage = (df.isna().sum()/shape_data[0])*100
            logging.info("Missing Data Number :- "+str(df.isna().sum()))
            logging.info("Missing Data Percentage :- "+str(missing_percentage)+"%")
            logging.info("Column Names"+df.columns)
            logging.info("Converting Categorical to Numerical")
            x=df.drop(["prices"],axis=1)    
            x_cols=x.columns
            converted_json={}
            df1 =df.copy()
            for itr in x_cols:
                df_main=self.convert_categorical(itr,df,df1)
                df=df_main[0]
                df1=df_main[1]
                med = df_main[2]
                converted_json[itr]=med.to_dict()
            json_object = json.dumps(converted_json, indent=4)
 
            # Writing to sample.json
            with open(self.data_pre_processing_config.convert_json_file, "w") as outfile:
                outfile.write(json_object)
            
            df = df.sort_values('brand_name', ascending=True).reset_index(drop=True)

            df1 = df1.sort_values('brand_name', ascending=True).reset_index(drop=True)
            
            logging.info("Taking out null values")
            df_null=df[df['prices'].isnull()]
            df1_null=df1[df1['prices'].isnull()]
            
            logging.info("drop the prices")
            df.dropna(subset=['prices'],inplace=True)
            df1.dropna(subset=['prices'],inplace=True)
            logging.info("Imputing the Missing values")
            
            #Filling the columns with m
            imputer = KNNImputer(n_neighbors=2)
            df = imputer.fit_transform(df)
            df=pd.DataFrame(df)
            df.columns=['brand_name','processor_brand',"ram","os","storage","prices"]

            df= df.astype("int")

            
            df1 = imputer.fit_transform(df1)
            df1=pd.DataFrame(df1)
            df1.columns=['brand_name','processor_brand',"ram","os","storage","prices"]
            df1= df1.astype("int")

            # df_null = imputer.fit_transform(df_null)
            # df_null=pd.DataFrame(df_null)
            # df_null.columns=['brand_name','processor_brand',"ram","os","storage","prices"]
            # df_null= df_null.astype("int")

            # df1_null = imputer.fit_transform(df1_null)
            # df1_null=pd.DataFrame(df1_null)
            # df1_null.columns=['brand_name','processor_brand',"ram","os","storage","prices"]
            # df1_null= df1_null.astype("int")
            

            logging.info("After Imputing the missing values ..............")
            shape_data = df.shape
            
            logging.info(" Row :- "+str(shape_data[0])+", Columns:- "+str(shape_data[1]))
            missing_percentage = (df.isna().sum()/shape_data[0])*100
            logging.info("Missing Data Number :- "+str(df.isna().sum()))
            logging.info("Missing Data Percentage :- "+str(missing_percentage)+"%")
            
            #storing it

            os.makedirs(self.data_pre_processing_config.artifact_file_path_processing_main ,exist_ok=True)
            os.makedirs(self.data_pre_processing_config.artifact_file_path_processing_main_dataset, exist_ok=True)
            os.makedirs(self.data_pre_processing_config.artifact_file_path_processing_main_dataset_null,exist_ok=True)
            df.to_csv(path_or_buf=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_data,index=False,header=True)
            df1.to_csv(path_or_buf=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_data_1,index=False,header=True)
            df_null.to_csv(path_or_buf=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_null_data,index=False,header=True)
            df1_null.to_csv(path_or_buf=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_null_data_1,index=False,header=True)
            
            data_pre_processing_artifact=predict_artifact_config.DataPreProcessingArtifact(feature_store_file_path_data=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_data,
                                                                                           feature_store_file_path_null_data=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_null_data,
                                                                                           feature_store_file_path_null_data_1=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_null_data_1,
                                                                                           feature_store_file_path_data_1=self.data_pre_processing_config.artifact_file_path_processing_main_dataset_data_1,
                                                                                           feature_converting_category=self.data_pre_processing_config.convert_json_file)
            return data_pre_processing_artifact



        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
    
    def convert_categorical(self,col_name,df,df1):
        logging.info(col_name+" Started:- ")
        
        n=df[col_name].unique()
        #taking out nan rows
        rows_with_nan = df[df[col_name].isna()]
    
        #dropping the nan rows
        df.dropna(subset=[col_name],inplace=True)
        df1.dropna(subset=[col_name],inplace=True)
        #creating a mean -median price dataframe
        Memmory=[]
        Median=[]
        mean=[]
        Mean_Median_Prices =[]
        for itr in n:
            Memmory.append(itr)
            a=df[df[col_name]==itr]
            Median.append(a['prices'].median())
            mean.append(a['prices'].mean())
            Mean_Median_Prices.append((a['prices'].median()+a['prices'].mean())/2)

        med=pd.DataFrame(list(zip(Memmory,Median,mean,Mean_Median_Prices)),columns=[col_name,'Median Prices','Mean Prices',"Mean_Median_Prices"])
        #creating bins

        bin_edges = [med['Mean_Median_Prices'].min()-1, med['Mean_Median_Prices'].quantile(.10), med['Mean_Median_Prices'].quantile(.20),med['Mean_Median_Prices'].quantile(.30),med['Mean_Median_Prices'].quantile(.40),   med['Mean_Median_Prices'].quantile(.5), med['Mean_Median_Prices'].quantile(.60), med['Mean_Median_Prices'].quantile(.70),med['Mean_Median_Prices'].quantile(.80),med['Mean_Median_Prices'].quantile(.90),  med['Mean_Median_Prices'].max()]
        med['Mean_Median_Prices_groups'] = pd.cut(med['Mean_Median_Prices'], bins=bin_edges)
        med
        uni=0
        
        for index,itr  in med.iterrows():
            
            df1[col_name]=df1[col_name].replace(itr[col_name],uni)
            uni+=1
        
        uni = 0
        for itr in med['Mean_Median_Prices_groups'].unique():
            
            med['Mean_Median_Prices_groups']=med['Mean_Median_Prices_groups'].replace(itr,uni)
            uni+=1
        

        for index,itr  in med.iterrows():
            
            df[col_name] = df[col_name].replace(itr[col_name],itr['Mean_Median_Prices_groups'])
        df = pd.concat([df,rows_with_nan])
    
        df1= pd.concat([df1,rows_with_nan])
        logging.info(col_name+"Ended ....")
        print(med)
        return [df,df1,med[[col_name,'Mean_Median_Prices_groups']]]
        