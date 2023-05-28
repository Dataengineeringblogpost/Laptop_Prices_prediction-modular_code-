from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
import sys
from Scrapers.scrape_component.scrape_flipkart import *
from Scrapers.scrape_entity import scrape_config_entity
from Scrapers.scrape_component.scrape_reliance import *
from Scrapers.scrape_component.scrape_combine import *
       
class main_scrape:
    def main(self):
        try:
            scrapper=scrape_config_entity.ScraperPipelineConfig()
            DataBaseConfig=scrape_config_entity.DataBaseConfig(scrapper)
            print(DataBaseConfig.to_dict())
            flipkart_scrape=flipkart_scraper(DataBaseConfig)
            flipkart_data=flipkart_scrape.main()
            
            reliance_scrappe = reliance_scraper(DataBaseConfig=DataBaseConfig)
            reliance_data=reliance_scrappe.main()
            reliance_data_store = reliance_data.data_store
            flipkart_data_store = flipkart_data.data_store
            conbine=excel_combine(DataBaseConfig=DataBaseConfig)
            combine_data = conbine.combine(reliance_data_store,flipkart_data_store)
           
            data_file = combine_data.data_store
            return data_file


        except Exception as e:
            print(str(e))
            print("Error occoured")
            logging.debug(str(e))