import pandas as pd
import numpy as np
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from Laptop_Price_Prediction import predict_utils
import sys
import os
from Laptop_Price_Prediction.predict_entity import predict_artifact_config


class DataTransformation:
    def __init__(self,data_ingestion_artifact,data_transformation_config):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

    """
    Objective:- 
    1) Calling the ingestion .csv file and Creating a Dataframe.
    2) Transforming all columns .
    """
    def intitate_data_transformation(self):
        try:
            logging.info("Calling the ingestion .csv file and Creating a Dataframe ")
            df=pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)
            
            #Brand Name
            logging.info("Transforming Brand Name")
            df['brand_name']=df['0'].apply(self.title_to_brand)
           
           
            col_name = "brand_name"
            
            predict_utils.del_rows_count(df,col_name)  
            
            #Processor_Brand
            logging.info("Transforming Processor ")
            df['1']=df['1'].replace("Free upgrade to Windows 11* when available",np.NaN)  
            df["processor_brand"]=df['1'].apply(self.get_intel)
            df["processor_brand"]=df["processor_brand"].apply(self.get_apple)
            df["processor_brand"] = df['processor_brand'].replace("intel ryzen 7 quad core processor","amd ryzen  7  quad")
            df["processor_brand"]=df["processor_brand"].apply(self.get_amd)
            
            #RAM
            logging.info("Transforming RAM ")
            df['2']=df['2'].apply(self.get_ram)

            # OS
            logging.info("Transforming OS ")
            df['3']=df['3'].apply(self.get_os)

            #Storage
            logging.info("Transforming Storage ")
            df['4']=df['4'].apply(self.get_storage)

            #Prices
            logging.info("Transforming Prices ")
            df['5'] =df['5'].replace('[\$,]', '', regex=True).astype(float)
            

            #storing it
            os.makedirs(self.data_transformation_config.artifact_folder_path_DataTransformation ,exist_ok=True)
            os.makedirs(self.data_transformation_config.artifact_database_folder_path_DataTransformation,exist_ok=True)
            df.to_csv(path_or_buf=self.data_transformation_config.artifact_database_file_path_DataTransformation,index=False,header=True)
            data_transformation_artifact=predict_artifact_config.DataTransformationArtifact(feature_store_file_path=self.data_transformation_config.artifact_database_file_path_DataTransformation,)
            return data_transformation_artifact
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)

    #Brand Name :- converting title to brand
    def title_to_brand(self,title):
        brand_name=str(title).split(" ")[0].lower()
        if "new" in   brand_name:
            return  str(title).split(" ")[1].lower()
        return brand_name
    

    #Transforming Processor
    def get_intel(self,processor):
        processor=str(processor).lower()
        main_str = ""
        proc_types = ['i3',"i5","i7","i9","celeron","pentium"]
        gen_types = ['10th',"11th","12th","13th"]
        main_str="intel"
        if "ryzen" not in processor:
            if "i3" in processor or "i5" in processor or "i7" in processor or "i9" in processor or "celeron" in processor or "intel" in processor:
                for proc in proc_types:
                    if proc in processor:
                        main_str = main_str + " "+ proc
                for gen in gen_types:
                    if gen in processor:
                        main_str = main_str +" "+ gen
                if len(main_str)==5:
                    return processor
                else:
                    return main_str
            else:
                return processor
        else:
            return processor
        
    def get_apple(self , processor):
        main_str=""
        chips = ['m1','m2']
        processor=str(processor).lower()
        if "apple" in processor:
            main_str = main_str+"apple"
            for chip in chips:
                if chip in processor:
                    main_str= main_str +" "+ chip
            return main_str
        else:
            return processor
    
    def get_amd(self,processor):
        
        processor = processor.replace("-"," ")
        processor = processor.replace("ryzen7","ryzen 7")
        main_str = ""
        cores = ["dual","hexa","quad","octa"]
        numbers=[" 3 "," 5 "," 7 "," 9 "]
        processor_split = processor.split(" ")
        if "amd" in processor or "ryzen" in processor:
            if "amd ryzen" in processor:
                
                main_str = "amd ryzen"
                for number in numbers:
                    if number in processor:
                        main_str = main_str+" "+number
                for core in cores:
                    if core in processor:
                        main_str = main_str +" "+core
                return main_str
        
                
            else:
                return processor
        else:
            return processor
    
    #Transforming RAM
    def get_ram(self , ram):
        ram = str(ram)
        ram = ram.strip(" ")
        ram = ram.replace("4GB","4 GB")
        ram = ram.replace("8GB","8 GB")
        ram = ram.replace("16GB","16 GB")
        ram = ram.replace("32GB","32 GB")
        ram = ram.replace("64GB","64 GB")
        return ram[:2]
    
    #Transsforming OS
    def get_os(self,os):
        os = str(os)
        main_str  =   ""
        window_types=['11','10']
        os=os.lower()
        if "windows" in os or "window" in os:
            main_str= main_str+"Windows"
            for window_type in window_types:
                if window_type in os:
                    main_str=main_str+" "+window_type
        elif "macos" in os or "mac os" in os:
            main_str="macos"
            
        elif "dos" in os:
            main_str="dos"
        elif "chrome" in os:
            main_str="chrome"
        else:
            main_str = os
        return main_str
    
    #Transforming Storage
    def get_storage(self,storage):
        storage = str(storage).lower()
        storage = storage.split("|")[0]
        storage = storage.split("+")[0]
        storage = storage.split(",")[0]
        storage = storage.replace("128gb","128 gb")
        storage = storage.replace("512gb","512 gb")
        storage = storage.replace("256gb","256 gb")
        storage = storage.replace("1tb","1 tb")
        storage = storage.replace("512 gb ssd ssd","512 gb ssd")
        storage = storage.replace("512 ssd","512 gb ssd")
        storage = storage.replace("1 tb pcie nvme m.2 ssd","1 tb ssd")
        storage = storage.replace("128 gb","128 gb ssd")
        storage= storage.replace("128 gb ssd 128 gb ssd emmc","128 gb ssd")
        
        return storage
    
