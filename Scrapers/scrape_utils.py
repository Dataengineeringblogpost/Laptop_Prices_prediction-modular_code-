from selenium import webdriver
import pymysql
from bs4 import BeautifulSoup
import requests
import pandas as pd
class utils:
    def get_chrome_driver():
        driver=webdriver.Chrome()
        return driver

    @staticmethod
    def pymysql_cred(database_name):
        conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "karthiksara@2123",
        db = database_name
        )
        
        return conn
     
    
    
    @staticmethod
    def create_tables(main_table_name,specific_table_name,database_name):
        conn=utils.pymysql_cred(database_name)
        cur=conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS '+main_table_name +' (Title VARCHAR(8955),Processor  VARCHAR(255),RAM VARCHAR(255),Operating_System  VARCHAR(255),Memmory  VARCHAR(255),Prices  VARCHAR(255))')
        conn.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS '+specific_table_name +' (Title VARCHAR(8955),Processor  VARCHAR(255),RAM VARCHAR(255),Operating_System  VARCHAR(255),Memmory  VARCHAR(255),Prices  VARCHAR(255))')
        conn.commit()


    #Exporting the data putting it into artifact 
    @staticmethod
    def export_data(table_name,export_excel,database_name):
        print(database_name)
        conn=utils.pymysql_cred(database_name)
        cur = conn.cursor()
        query = "SELECT * FROM "+ table_name
        cur.execute(query)
        table_rows = cur.fetchall()
        df = pd.DataFrame(table_rows)
    
        df.to_excel(export_excel+".xlsx")
        return "Done"
    
