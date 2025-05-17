import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.CustomException import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger=get_logger(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/instance/Desktop/gcp_key/model-choir-456708-p0-6635765bc682.json"
class DataIngestion:
    def __init__(self, config):
        self.config=config['data_ingestion']
        self.bucket_name=self.config['bucket_name']
        self.bucket_file_name=self.config['bucket_file_name']
        self.train_test_ratio=self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion Started with {self.bucket_name} and file is {self.bucket_file_name}")

    def csv_download_gcp(self):
        try:
            client=storage.Client()
            bucket=client.bucket(self.bucket_name)
            blob=bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info("Raw file successfully downloaed")
        except Exception as e:
            logger.error('Error while downloading file')
            raise CustomException('Failed to download file',e)
        
    def data_split(self):
        try:
            logger.info('Starting Data Splitting')
            data=pd.read_csv(RAW_FILE_PATH)
            train_data,test_data=train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Train data saved to Train File Path")
            logger.info(f"Test data saved to Test File Path")


        except Exception as e:
            logger.error('Error while Data Spliting')
            raise CustomException('Failed to Split the Data into Train and Test',e)

    def run(self):
        try:
            logger.info('Data Ingestion Process Begin')
            self.csv_download_gcp()
            self.data_split()
            logger.info('Data Ingestion Compleated')
        except Exception as ce:
            logger.info('Data Ingestion is Incompleate')
            raise CustomException(f"Data Ingestion have some fatal issue", str(ce))
        

if __name__ == "__main__":
    try:
        logger.info('Data Ingestion Method is Executing')
        data_ingestion=DataIngestion(read_yaml(CONFIG_PATH))
        data_ingestion.run()  # <- Make it 0 if you want to test error
        logger.info('Data Ingestion Process Compleated')

    except CustomException as ce:
        logger.error(str(ce))



