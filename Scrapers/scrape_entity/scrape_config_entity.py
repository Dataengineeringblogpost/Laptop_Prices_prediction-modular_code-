import os
import sys
from datetime import datetime
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
import random
class ScraperPipelineConfig:

    def __init__(self) :
        try:
            rnumber=random.randint(0, 9000)
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m$d%Y_%H%M')}{rnumber}")
            os.makedirs(self.artifact_dir,exist_ok = True)
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        

class DataBaseConfig:
    def __init__(self,ScraperPipelineConfig:ScraperPipelineConfig):
        try:
            
            self.artifact_dir=ScraperPipelineConfig.artifact_dir
            self.database_name = "laptop_price_prediction"
            self.main_table_name = "laptop_data"
            self.specific_flipkart_table_name = "flipkart_laptop_data"
            self.specific_reliance_table_name = "reliance_laptop_data"
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
    
    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
    
# class FlipkartConfig:
#     def __init__(self,ScraperPipelineConfig:ScraperPipelineConfig):
#         try:
#             self.specific_flipkart_table_name = "flipkart_laptop_data"
#         except Exception as e:
#             raise Laptop_Price_Prediction_Exception(e,sys)
