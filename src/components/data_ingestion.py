import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import  dataclass #used to create class variable
from src.components.data_transformation import DataTransformation

@dataclass #as we are only defining variables so we use dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv(r'D:\Coding\ML-Project\notebooks\data\stud.csv')
            logging.info('Read the dataset from csv')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)#dont delete if exist  
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True) #index means row number and header means column name
            logging.info('Train test split initiated')

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    obj = DataIngestion()
    train_data_path,test_data_path = obj.initiate_data_ingestion()
    transformation_obj = DataTransformation()
    transformation_obj.initiate_data_transformation(train_data_path,test_data_path)

