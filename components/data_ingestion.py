import os
import sys 
import pandas as pd
import numpy as np
from dataclasses import dataclass
#from pathlib import Path
import logging
from sklearn.model_selection import train_test_split



@dataclass
class DataIngestionConfig:
    """
    Class that define path and define directory and csv files for data
    """ 
    immoblier_data_path: str = os.path.join("artifacts", "immoblier.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")


class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data ingestion started")
        try:
            data = pd.read_csv("/home/marwane/mlops-projects/morocco-appartements-price/data-houses-price-orgnised-not-prepared.csv", low_memory=False)
            
            try:
                os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.immoblier_data_path)))
            except:
                pass

            data.to_csv(self.ingestion_config.immoblier_data_path, index=False)
            
            train_data, test_data = train_test_split(data, test_size=.2) # random_state=42

            # save splited data
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("The data is splited into train and test set")

            #print(train_data.head(1))
            #print("-----------------------")
            #print(test_data.head(1))

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            print(e)



"""
if __name__ == "__main__":
    obj_data_ingest = DataIngestion()
    obj_data_ingest.initiate_data_ingestion()"""