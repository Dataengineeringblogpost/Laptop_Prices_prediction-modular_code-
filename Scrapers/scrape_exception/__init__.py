import os
import sys
"""
This is where we create the call for basic exception handling
"""

class   Laptop_Price_Prediction_Exception(Exception):

    #Creating a constructor
    def __init__(self, error_message:Exception, error_detail:sys):
        
        #Calling the static method
        """
        error_message=error
        error_detail:error details via exception
        """
        self.error_message = (Laptop_Price_Prediction_Exception.error_message_detail(error_message, error_detail=error_detail))



    @staticmethod
    def error_message_detail(error:Exception, error_detail:sys)->str:
        """
        error: Exception object raise from module
        error_detail: is sys module contains detail information about system execution information.
        here we are basically create a error message that will be stored in the log file if an error occours
        """
        _, _, exc_tb = error_detail.exc_info()
        #get line number of the error
        line_number = exc_tb.tb_frame.f_lineno
    
        #extracting file name from exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename 

        #preparing error message
        error_message = f"Error occurred python script name [{file_name}]" \
                        f" line number [{exc_tb.tb_lineno}] error message [{error}]."

        return error_message