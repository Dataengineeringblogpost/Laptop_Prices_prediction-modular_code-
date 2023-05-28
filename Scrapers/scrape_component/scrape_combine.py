import pandas as pd
from Scrapers.scrape_entity.scrape_config_entity import *
from Scrapers.scrape_entity.scrape_artifact_entity import *
from Scrapers.scrape_logger import logging
import random
class excel_combine:
    def __init__(self,DataBaseConfig):
        self.excel_list = []
        self.excel_l=[]
        self.DataBaseConfig = DataBaseConfig
        self.artifact_dir = self.DataBaseConfig.artifact_dir



    def combine(self,reliance_data_store,flipkart_data_store):
        try:
            logging.info("Starting to combine excel files")
            self.excel_l.append(reliance_data_store)
            self.excel_l.append(flipkart_data_store)
            

            for file in self.excel_l:
                self.excel_list.append(pd.read_excel(file))
            excl_merged = pd.concat(self.excel_list, ignore_index=True)
            
            # exports the dataframe into excel file
            # with specified name.
            rnumber=random.randint(0, 9000)
            dataset=str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H%M'))+str(rnumber)+"main_laptop_data.xlsx"
            excl_merged.to_excel(dataset, index=False)
            mainArtifact = MainArtifact(data_store=dataset)
            print(mainArtifact)
            logging.info("Combined excel sucessfully")
            
            return mainArtifact
        except Exception as e:
            print("Error occoured")
            raise Laptop_Price_Prediction_Exception(e,sys)