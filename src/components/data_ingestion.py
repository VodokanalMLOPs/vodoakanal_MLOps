import os
import sys
from src.components.model_trainer import ModelTrainer
from src.exceptions import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'data.csv')
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entering data ingestion')
        try:
            df=pd.read_excel('notebook\data_new_v1.xlsx')
            logging.info('Reading data')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info('Train test split initalization')

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=69)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Data Ingesttion completed')

            return(self.ingestion_config.train_data_path,
                   self.ingestion_config.test_data_path)
        except CustomException as e:
            raise CustomException(e, sys)
        

if __name__=='__main__':
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_tranformation = DataTransformation()
    train_arr,test_arr,_ = data_tranformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
