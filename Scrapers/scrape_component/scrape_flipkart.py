from turtle import title
from webbrowser import get
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymysql
from Scrapers.scrape_utils import *
from Scrapers.scrape_exception import Laptop_Price_Prediction_Exception
from Scrapers.scrape_logger import logging
from Scrapers.scrape_entity.scrape_config_entity import *
import sys
from datetime import datetime
import openpyxl
from Scrapers.scrape_entity.scrape_artifact_entity import *

class flipkart_scraper:

    def __init__(self,DataBaseConfig) :
        self.title_data=[]
        self.count=3
        self.DataBaseConfig = DataBaseConfig
        # self.FlipkartConfig = FlipkartConfig
       

        self.main_table_name=self.DataBaseConfig.main_table_name
        self.specific_flipkart_table_name = self.DataBaseConfig.specific_flipkart_table_name
        self.database_name = self.DataBaseConfig.database_name
        self.artifact_dir = self.DataBaseConfig.artifact_dir

    """
    Objective:-Creating tables if not created
    """
    def create_dt(self):
        try:
            
            utils.create_tables(self.main_table_name,self.specific_flipkart_table_name,self.database_name)
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        
     
    """
    Objective:-checking wheather to update the data or to totally scrape it ...
    depending upon the lebght of the data
    """
    def check_data(self):
        try:
            
            conn=utils.pymysql_cred(self.database_name)
            cur = conn.cursor()
            query = "SELECT Title FROM "+  self.specific_flipkart_table_name
            cur.execute(query)
            result = cur.fetchall() 
            
            final_result = [i[0] for i in result]
            
            if len(final_result) >= 50:
                return True
            else:
                return False
        except Exception as e:
            raise Laptop_Price_Prediction_Exception(e,sys)
        
    def get_data(self,url):
        data=requests.get(url)
        soup=BeautifulSoup(data.content,'html.parser')
        data=soup.find_all(class_="_2kHMtA")
        return data

    def main(self):
        logging.info("Starting Flipkart data scraping ...")
        #Creating a table 
        self.create_dt()
        #checking wheather to update the data or to totally scrape it ...
        check=self.check_data()
        
        if not check:

            try:
                #Here we are scraping the data
                logging.info("Scraping the Flipkart data")
                for iter in range(0,100): 
                    
                    url = 'https://www.flipkart.com/search?q=laptop&sort=recency_desc&page='+ str(iter)
                    data_laptop = self.get_data(url)
                    final_data = self.build_laptop_data(data_laptop,iter)
                    
                    if final_data == 'Done':
                        logging.info("Scraped "+str(iter)+" Pages")
                        logging.info("Flipkart scraping sucessfully ended ✔️")
                        break
                    else:
                        print( "✔️ page "+ str(iter) +" data inserted into the table ")
                print(self.artifact_dir+str(datetime.now().strftime('%m$d%Y_%H%M%S'))+"flipkart_data")
                self.export_data(self.specific_flipkart_table_name,self.artifact_dir+str(datetime.now().strftime('%m$d%Y_%H%M%S'))+"flipkart_data")
                logging.info("Flipkart File exported to Artifact")
                flipkartArtifact = FlipkartArtifact(data_store=str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H%M%S'))+"flipkart_data.xlsx")
                return flipkartArtifact
                
            except Exception as e:
                raise Laptop_Price_Prediction_Exception(e,sys)
        else:
            #Here we are updating it
            logging.info("Updating the Flipkart data")
          
            try:
                for iter in range(0,100): 
                    url = 'https://www.flipkart.com/search?q=laptop&sort=recency_desc&page='+ str(iter)
                    data_laptop = self.get_data(url)
                    final_data = self.build_updated_laptop_data(data_laptop,iter)
                    
                    if final_data == 'Done':
                        logging.info("Scraped "+str(iter)+" Pages")
                        logging.info("Flipkart scraping sucessfully ended ✔️")
                        break
                    else:
                        print( "✔️ page "+ str(iter) +" data inserted into the table ")
                print(self.artifact_dir+str(datetime.now().strftime('%m$d%Y_%H%M%S'))+"main_data")
                
           
                self.export_data(self.specific_flipkart_table_name,str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"flipkart_data")
                logging.info("Flipkart File exported to Artifact")
                flipkartArtifact = FlipkartArtifact(data_store=str(self.artifact_dir+"\\"+datetime.now().strftime('%m$d%Y_%H'))+"flipkart_data.xlsx")
                return flipkartArtifact
            except Exception as e:
                raise Laptop_Price_Prediction_Exception(e,sys)

 
    """
    Objective:-Here we are building/Cleaning our data and returning our data in a  dictionary format
    then sending the dictionary to store in the database
    """
    def build_laptop(self,itre,title_data):
        #Template dictionary data
        data={"Title":" ","Rating":" ","Out_of_rating":" ","Processor":" ","RAM":" ","Operating_System":" ","Display":" ","Memory":" "
                    ,"Warranty":" ","Others":" ","Prices":""}
        words=''
        others=''
        #getting price from our data
        price=itre.find(class_='_30jeq3 _1_WHN1')
        rating=itre.find("div",{'class':'_3LWZlK'})
        out_of_rating=itre.find(class_='_2_R_DZ')
        get_desc=itre.find_all('li',{'class':'rgWa7D'})
        rating_data=rating.text if rating is not None else ""
        #Updating our dictionary 
        data['Title']=title_data
        self.title_data.append(title_data)
        data['Rating']=rating_data
        price_data=price.text[1:] if price is not None else " "
        data['Prices']=price_data
        out_of_rating_data=out_of_rating.text.split(" ")[0] if out_of_rating is not None else " "
        data['Out_of_rating']=out_of_rating_data

        for itr in get_desc:
            if "Processor" in itr.text:
                Processor=itr.text if itr is not None else ""
                data["Processor"]=Processor
            elif "RAM" in itr.text:
                RAM=itr.text if itr is not None else ""
                data['RAM']=RAM
                continue
            elif "Operating System" in itr.text:
                OS=itr.text if itr is not None else ""
                data["Operating_System"]=OS
                continue
            elif "Display" in itr.text:
                Display=itr.text if itr is not None else ""
                data["Display"]=Display
                continue
            elif "Warranty" in itr.text:
                Warranty=itr.text if itr is not None else ""
                data["Warranty"]=Warranty
                continue
            elif "SSD"  in itr.text:
                Memory=itr.text if itr is not None else ""
                data["Memory"]=Memory
                continue
            elif "HDD" in itr.text:
                Memory=itr.text if itr is not None else ""
                data["Memory"]=Memory
                continue
            else:
                words=itr.text if itr is not None  else ""
                others=others+words+" , "
        data['Others']=others
        #Saving the data to our database
        self.save_laptop_data(data)
    
    """
    Objective:-Checking wheather our data is repeated or not if its repeated then we are eaarly stoping the data
    its checking for updated scrape so 3 chances are given
    """
    def build_updated_laptop_data(self,data_laptop,iter):
        #df=pd.DataFrame(columns=["Title","Rating","Out_of_rating","Processor","RAM","Operating_System","Display","Memory","Warranty","Others","Prices"])

        if len(data_laptop)!=0:
            self.count=3

            for itr in data_laptop:
                title=itr.find_all(class_='_4rR01T')
                title_data=title[0].text
            
                print(title_data)
                if title_data not in self.title_data :
                    self.build_laptop(itr,title_data)
                    
                else:
                    return 'Done'

            
        else:

            self.count=self.count-1
            if self.count==0:
                return 'Done'
    
    """
    Objective:-Checking wheather our data is repeated or not if its repeated then we are eaarly stoping the data
    its checking for normal scrape so 5 chances are given
    """
    def build_laptop_data(self,data_laptop,iter):
        if len(data_laptop)!=0:
            self.count=5

            for itr in data_laptop:
                title=itr.find(class_='_4rR01T')
                title_data=title.text if title is not None  else ""
                self.build_laptop(itr,title_data)
        else:

            self.count=self.count-1
            if self.count==0:
                return 'Done'
        
    #Saving the data into the database
    def save_laptop_data(self,data):
        
        conn=utils.pymysql_cred(self.database_name)
        cur = conn.cursor()
        sql = "INSERT INTO  "+self.specific_flipkart_table_name+"(Title,Processor,RAM,Operating_System,Memmory,Prices) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (str(data['Title']),str(data['Processor']),str(data['RAM']),str(data['Operating_System']),str(data['Memory']),str(data['Prices']))
        cur.execute(sql, val)
        conn.commit()
        sql = "INSERT INTO  "+self.main_table_name+"(Title,Processor,RAM,Operating_System,Memmory,Prices) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (str(data['Title']),str(data['Processor']),str(data['RAM']),str(data['Operating_System']),str(data['Memory']),str(data['Prices']))
        cur.execute(sql, val)
        conn.commit()
    
    #Exporting the data putting it into artifact 
    def export_data(self,table_name,export_excel):
        conn=utils.pymysql_cred(self.database_name)
        cur = conn.cursor()
        query = "SELECT * FROM "+ table_name
        cur.execute(query)
        table_rows = cur.fetchall()
        df = pd.DataFrame(table_rows)
        print(df)
        df.to_excel(export_excel+".xlsx")
        return "Done"