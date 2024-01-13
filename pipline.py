import pandas as pd
import logging
import os
import yaml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
import numpy as np


class DataProcessor:
    def __init__(self, config_file_path):
        self.config = self.load_config(config_file_path)
        self.initialize_logging()

    def load_config(self, file_path):
        """Load configuration from a YAML file."""
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def initialize_logging(self):
        """Set up logging configurations."""
        log_dir = './log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, 'data_log.log')

        # Reset log file
        with open(log_file, 'w') as file:
            pass

        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def convert_data_types(self, dataframe, to_int_cols, to_object_cols):
        """
        Convert specified columns of a DataFrame to different data types.
            
        Parameters:
        dataframe (pd.DataFrame): The DataFrame to be modified.
        to_int_cols (list): List of column names to convert to int64.
        to_object_cols (list): List of column names to convert to object.
        """
        # Ensure the columns exist in the dataframe
        existing_cols = dataframe.columns

        # Convert columns to int64 if they exist in the dataframe
        for col in to_int_cols:
            if col in existing_cols:
                dataframe[col] = dataframe[col].astype('int64')

        # Convert columns to object if they exist in the dataframe
        for col in to_object_cols:
            if col in existing_cols:
                dataframe[col] = dataframe[col].astype('object')
