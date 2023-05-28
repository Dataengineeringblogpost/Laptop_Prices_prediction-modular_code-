#Importing Modules
import requests
from requests.structures import CaseInsensitiveDict
from Scrapers.scrape_utils import *
import pymysql
import numpy as np
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from Scrapers.scrape_entity.scrape_config_entity import *
import openpyxl
from Scrapers.scrape_entity.scrape_artifact_entity import *
from functools import reduce

#Creating a Class
class reliance_scraper:
    def __init__(self,DataBaseConfig):

        self.DataBaseConfig = DataBaseConfig
        self.main_table_name=self.DataBaseConfig.main_table_name
        self.specific_reliance_table_name = self.DataBaseConfig.specific_reliance_table_name
        self.database_name = self.DataBaseConfig.database_name
        self.artifact_dir = self.DataBaseConfig.artifact_dir
        self.count_ = 15

    """
    Objective:-Creating tables if not created
    """
    def create_dt(self):
        try:
            
            utils.create_tables(self.main_table_name,self.specific_reliance_table_name,self.database_name)
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        
    """
    Objective :- this is our main function 
    """
    def main(self):
        try:

            logging.info("Starting Reliance data scraping ...")
            logging.info("Creating a Table  ")
            #Creating a table only if 
            self.create_dt()
            #Creating a Loop 0-1000
            for itr in range(0,1000):
                if self.count_ >= 0 :
                    #get_data:-it will scrape out the data 
                    data=self.get_data(itr)
                    #build_laptop :- building laptop data
                    dat=self.build_laptop(data)
                    
                    logging.info("✔️ page "+ str(itr) +" data inserted into the table ")
                    if dat=="done":
                        logging.info("Ending Reliance data scraping ...")
                        logging.info(str(itr)+" Pages Scraped")

                        utils.export_data(self.specific_reliance_table_name,str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"reliance_data",self.database_name)
                        logging.info("Reliance File exported to Artifact")
                        relianceArtifact = RelianceArtifact(data_store=str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"reliance_data.xlsx")
                        return relianceArtifact
                else:
                    logging.info("Ending Reliance data scraping ...")
                    logging.info(str(itr)+" Pages Scraped")
                    utils.export_data(self.specific_reliance_table_name,str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"reliance_data",self.database_name)
                    logging.info("Reliance File exported to Artifact")
                    relianceArtifact = RelianceArtifact(data_store=str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"reliance_data.xlsx")
                    return relianceArtifact
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)        
             
    
    """
    Objective:- here we are scraping data from a api
    """
    def get_data(self,itr):
            
            url = "https://www.reliancedigital.in/rildigitalws/v2/rrldigital/cms/pagedata?pageType=categoryPage&categoryCode=S101210&searchQuery=%3Arelevance%3Aavailability%3AExclude%20out%20of%20Stock&page="+str(itr)+"&size=24&pc="

            headers = CaseInsensitiveDict()
            headers["authority"] = "www.reliancedigital.in"
            headers["accept"] = "*/*"
            headers["accept-language"] = "en-US,en;q=0.9"
            headers["content-type"] = "application/json"
            # headers["cookie"] = "version=4.3.1; AKA_A2=A; HttpOnly; _gcl_au=1.1.2036416069.1673181297; _gid=GA1.2.154578704.1673181298; WZRK_G=de32b71116e24f958cea3dd3a06b3c34; _fbp=fb.1.1673181297861.1391848469; citrix_ns_id_.reliancedigital.in_%2F_wat=AAAAAAUsvXOAB6ZLPrnX-IySpMB98oCVivsCviiyC6iAyrcAUjc99KDJOOCOkd9A3YSHK0Fbr2rvsY-qco1WP1ZBgVV8&; RT="z=1&dm=www.reliancedigital.in&si=e0fc7a70-0790-4f93-8917-beeb5fd79099&ss=lcncxsk4&sl=2&tt=698&obo=1&rl=1"; _ga=GA1.2.1835428295.1673181298; _dc_gtm_UA-27422335-1=1; _gat_UA-27422335-1=1; _uetsid=dc7d73308f5011edb87c59fdb8617db7; _uetvid=dc7d8ca08f5011eda2a4098c214b3517; WZRK_S_8R5-85Z-K95Z=%7B%22p%22%3A3%2C%22s%22%3A1673181297%2C%22t%22%3A1673181376%7D; _ga_1DPVQ3BW9G=GS1.1.1673181297.1.1.1673181410.22.0.0"
            headers["dnt"] = "1"
            headers["referer"] = "https://www.reliancedigital.in/laptops/c/S101210?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page="+str(itr)
            headers["sec-ch-ua"] = "Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"
            headers["sec-ch-ua-mobile"] = "?0"
            headers["sec-ch-ua-platform"] = "Windows"
            headers["sec-fetch-dest"] = "empty"
            headers["sec-fetch-mode"] = "cors"
            headers["sec-fetch-site"] = "same-origin"
            headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
            resp = requests.get(url, headers=headers)

            #Converting our data to json data
            json_data_str=resp.json()
            return json_data_str
    
    """
    Objective :- Here we are build processor data
    """
    def get_processor(self,graph):
        if "<li>" in graph:
            processor = graph.split("<li>")[1]
            processor = processor.split("</li>")[0]
        else:
            processor = graph.split("\\")[0]
            
        if "Processor:"  in processor:
            processor = processor.split("Processor:")[1]
        
        
            return processor.strip(" ")
        if "Processor :" in processor:
            processor = processor.split("Processor :")[1]
        
        
            return processor.strip(" ")
    
        return processor.strip(" ")
    
    """
    Objective :- Here we are build ram data
    """
    def get_ram(self,graph):
        if "<li>" in graph:
            if "<li>RAM:" in graph:
                ram = graph.split("<li>RAM:")[1]
                ram=ram.split("</li>")[0]
                return ram
            
        else:
            ram = graph.split("RAM:")[1]
            ram = ram.split("//")[0]
            return ram
        return np.nan
    
    """
    Objective :- Here we are build os data
    """
    def get_os(self,graph):
        if  "<li>" in graph:
            if "<li>Operating system:" in graph:
                os = graph.split("<li>Operating system:")[1]
                os=os.split("</li>")[0]
                return os
            elif "<li>Operating System:" in graph:
                os = graph.split("<li>Operating System:")[1]
                os=os.split("</li>")[0]
                return os
            elif "<li>Operating System :" in graph:
                os = graph.split("<li>Operating System :")[1]
                os=os.split("</li>")[0]
                return os
        else:
            os = graph.split("RAM:")[1]
            os = os.split("//")[0]
            return os
        return np.nan
    

    """
    Objective :- Here we are build memmory data
    """
    def get_memmory(self,graph):
        if "<li>" in graph:
            if "<li>internal storage:" and "<li>storage type:" in graph:
            
                memmory_gb = graph.split("<li>internal storage")[1]
                memmory_gb=memmory_gb.split("</li>")[0]
                memmory_type = graph.split("<li>storage type")[1]
                memmory_type=memmory_type.split("</li>")[0]
                memmory_gb = memmory_gb.strip(":")
                memmory_gb = memmory_gb.strip(" ")

                memmory_type = memmory_type.strip(":")
                memmory_type = memmory_type.strip(" ")
                memmory = memmory_gb + " "+memmory_type
                memmory = memmory.strip(":")
                memmory = memmory.strip(" ")
                return memmory
        
        return np.nan

    """
    Objective :- Here we are building data from get_data
    """
    def build_laptop(self,json_data_str):    
        #Template dictionary data
        data={"Title":" ","Processor":" ","RAM":" ","Operating_System":" ","Memory":" ","Prices":""}
        
        products=json_data_str['data']['productListData']['results']
        #if Length of product is 0 so we end the code 
        
        if len(products) == 0:
            self.count_=0
            return "done"
        
        for itr in range(len(products)):
            title=products[itr]['name']
            data["Title"] = title

            self.build_updated_laptop_data(title)
            
            price=products[itr]['price']['value']
            data["Prices"] = price
            graph=products[itr]['summary']
            if graph.startswith("<li>"):
                processor = self.get_processor(graph)
                data['Processor'] = processor
                ram = self.get_ram(graph)
                data['RAM']=ram
                ops=self.get_os(graph)
                data['Operating_System']=ops
                graph=graph.lower()
                memory=self.get_memmory(graph)
                data['Memory']=memory
                self.save_reliance_data(data=data)
                
                if self.count_<=0:
                   
                    return "done"
    
    """
    Objective :- here we are saving the data 
    """
    def save_reliance_data(self,data):
        conn=utils.pymysql_cred(self.database_name)
        cur = conn.cursor()
        sql = "INSERT INTO  "+self.specific_reliance_table_name+"(Title,Processor,RAM,Operating_System,Memmory,Prices) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (str(data['Title']),str(data['Processor']),str(data['RAM']),str(data['Operating_System']),str(data['Memory']),str(data['Prices']))
        cur.execute(sql, val)
        conn.commit()
        sql = "INSERT INTO  "+self.main_table_name+"(Title,Processor,RAM,Operating_System,Memmory,Prices) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (str(data['Title']),str(data['Processor']),str(data['RAM']),str(data['Operating_System']),str(data['Memory']),str(data['Prices']))
        cur.execute(sql, val)
        conn.commit()

    """
    Objective:- if we find duplicated data we will decrease the count by 1 once it 
    reaches 0 it will end the scraping
    """
    def build_updated_laptop_data(self,Title):
        one_title_data=Title
        conn=utils.pymysql_cred(self.database_name)
        cur = conn.cursor()
        query = "SELECT Title FROM "+ str(self.specific_reliance_table_name)
        cur.execute(query)
        table_rows = cur.fetchall()
        title_data=self.flatten_tuple(table_rows)
        title_data=list(title_data)
       
        if one_title_data  in title_data :
            self.count_=self.count_-1
            
    """
    Objective :- we are flattening the tuple 
    """
    def flatten_tuple(self,nested_tuple):
        def reducer(acc, val):
            if isinstance(val, tuple):
                return acc + self.flatten_tuple(val)
            else:
                return acc + (val,)
        return reduce(reducer, nested_tuple, ())