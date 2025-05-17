import os
from src.logger import get_logger
import traceback
import sys



class CustomException(Exception):
    def __init__(self, message, error:sys):
        super().__init__(message)
        self.message = self.get_error_details(message, error)

    @staticmethod
    def get_error_details(message, error:sys):
        _, _,exc_tb=sys.exc_info()
        fn=exc_tb.tb_frame.f_code.co_filename
        ln=exc_tb.tb_lineno
        return f"Error occur in {fn}, line nimber {ln}: {message}"

    def __str__(self):
        
        return self.message
        