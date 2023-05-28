import logging
from datetime import datetime
import os

"""
Creating a 'Laptop_Price' folder 
then we create log files inside the 'Laptop_Price' with a timestamp
"""

#Defining variables  for creating folder and file names
LOG_DIR="Laptop_Price_Logger"
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

#Creating a Folder 'Laptop_Price' only if it is not created 
os.makedirs(LOG_DIR,exist_ok=True)
#Create the complete file path
LOG_FILE_DIR=os.path.join(LOG_DIR,LOG_FILE_NAME)

#Create a Logger
logging.basicConfig(
    #file path
    filename=LOG_FILE_DIR,
    #write shld be the file mode
    filemode="w",
    #Format in which the log shld be stored
    format='%(asctime)s %(levelname)s %(name)s %(message)s', 
    #Level of the logger
    level=logging.DEBUG
) 