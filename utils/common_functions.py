import os
import pandas as pd
import yaml
from src.logger import get_logger
from src.CustomException import CustomException
from config.paths_config import *

logger=get_logger(__name__ )

#CONFIG_PATH='D:\MLOPS\config\config.yaml'
#print(CONFIG_PATH)
#CONFIG_PATH='config/config.yaml'

def read_yaml(CONFIG_PATH):
    try:
        print(CONFIG_PATH)
        if not (os.path.exists(CONFIG_PATH)):
            raise FileNotFoundError(f"File not found in the given path")
        
        with open(CONFIG_PATH, 'r') as yaml_file:
            config=yaml.safe_load(yaml_file)
            logger.info('Successfully loaded YAML file')
            return config
        
    except Exception as e:
        logger.error('error while reading YAML file')
        raise CustomException('Failed to read YAML file')

if __name__ == "__main__":
    try:
        logger.info('Main Program Executing')
        read_yaml(CONFIG_PATH)  # <- Make it 0 if you want to test error
        logger.info('Function Executed')

    except CustomException as ce:
        logger.error(str(ce))