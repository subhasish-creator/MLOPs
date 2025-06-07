import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.CustomException import CustomException
from utils.common_functions import load_data, read_yaml
from config.path_config import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger=get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config):
        self.train_path=train_path
        self.test_path=test_path
        self.processed_dir=processed_dir
        self.config=read_yaml(config)
        

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
        logger.info(f"Data Processing Started")

    def pre_process_data(self,df):
        try:
            logger.info(f"Starting Data Pre_Processing")
            logger.info(f"Droping columns")
       
            df.drop(columns=[
                            
                            'Unnamed: 0','arrival_date_year','arrival_date_week_number',
                            'arrival_date_day_of_month','country','assigned_room_type','agent','company','name','email','phone-number', 
                            'credit_card','reservation_status','reservation_status_date',
                            'country'
                            
                            ], inplace=True)
            df.drop_duplicates(inplace=True)
            df = df.dropna(axis=0)
            df = df[df['adr'] >= 0].reset_index(drop=True)
            cat_cols=self.config['data_processing']['categorical_columns']
            num_cols=self.config['data_processing']['numerical_columns']
            logger.info(f"cat_cols are {cat_cols}")
            logger.info(f"num_cols are {num_cols}")

            logger.info(f"Applying label Encoding")
            #le=LabelEncoder()
            mappings={}
          
            for col in cat_cols:
                import traceback
                le=LabelEncoder()
                traceback.print_exc

                df[col]=le.fit_transform(df[col])
                mappings[col]={label:code for label, code in zip(le.classes_,le.transform(le.classes_))}
            logger.info(f"Mappings are ....")
           
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info(f"Skewness Handling ....")

            skew_threshold=self.config['data_processing']['skewness_threshold']
            skewness=df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness>skew_threshold].index:
                df[column]=np.log1p(df[column])
            
            return df

        
        
        
        except Exception as e:
            logger.error('Error during Data Processing {e}')
            raise CustomException('Failed to preprocess data',e)

    def balanced(self,df):
        try:
            logger.info(f"Handling Data Imbalance")
            X=df.drop(columns='is_canceled')
            
            print('Missing in X ',X.isnull().sum())
            y=df['is_canceled']
            smote=SMOTE(random_state=42)
            X_resampled,y_resampled=smote.fit_resample(X,y)
            balanced_df=pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['is_canceled']=y_resampled

            logger.info('Data Balance is Compleated')

            return balanced_df
        
        except Exception as e:
            logger.error(f'Error during Data Balancing {e}')
            raise CustomException('Failed to preprocess data balancing',str(e))
      
    
    def feature_selection(self, balanced_df):
        try:
            logger.info(f"Beginig of Feature Selection")
            X=balanced_df.drop(columns='is_canceled')
            y=balanced_df['is_canceled']
            model=RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importances=model.feature_importances_
            fi_df=pd.DataFrame({'feature': X.columns,'importance':feature_importances})
            top_features_df=fi_df.sort_values(by='importance', ascending=False)
            num_of_features_select=self.config['data_processsing']['num_of_features']
            top_10_features=top_features_df['feature'].head(num_of_features_select).values
            top_10_df=balanced_df[top_10_features.tolist() + ['is_canceled']]
            

            logger.info(f"Feature Selection is Compleated Successfully")
            return top_10_df
        except Exception as e:
            logger.error(f" Error in feature selection {e}")
            raise CustomException(f"Error Feature Selection ,e")

    def data_save(self, df, file_path):
        try:
            logger.info('Saving the Processed File')
            df.to_csv(file_path, index=False)

            logger.info(f"Data Save Successfully.")
        except Exception as e:
            logger.error(f" Error in Saving file {e}")
            raise CustomException(f"Could not save the processed file, str(e)")
    
    
    def process(self):
        try:
            logger.info(f"Loading data from RAW directory")

            train_data=load_data(self.train_path)
            test_data=load_data(self.test_path)

            train_data=self.pre_process_data(train_data)
            test_data=self.pre_process_data(test_data)

            train_data=self.balanced(train_data)
            test_data=self.balanced(test_data)

            train_data=self.feature_selection(train_data)
            test_data=test_data[train_data.columns]

            train_data=self.data_save(train_data, PROCESSED_TRAIN_FILE_PATH)
            test_data=self.data_save(test_data,PROCESSED_TEST_FILE_PATH)

            logger.info(f"Data Processing Compleated Successsfully")

        except Exception as e:

            logger.info(f" Data Processing  Pipeline  error, {e}")
            raise CustomException("Data Processing Pipeline Have some Issue" , e)
        

if __name__ == "__main__":
    try:
        logger.info('Data Processing Method is Executing')
        data_processing=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
        data_processing.process()  
        logger.info('Data Processing Process Compleated')

    except CustomException as ce:
        logger.error(str(ce))

 




