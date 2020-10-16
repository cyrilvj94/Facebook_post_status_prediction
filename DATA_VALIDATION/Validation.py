import os
import pandas as pd
import numpy as np
import json
import shutil

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s : %(message)s')
file_handler = logging.FileHandler('LOGS/Data_validation_logs/data_validations.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Train_validation:
    """"
    This class is used for validating the raw training data.
    parameters: File Path containing Raw training data
    """
    def __init__(self, file_path):
        try:
            self.file_path = file_path
            logger.info("Created the Train Validation object ")
        except Exception as e:
            logger.error("Problem with object initialization {}".format(e))
            raise e

    def getvaluesfromjson(self):
        """"
        Description: To get the details of data from .json file
        Input: None
        Output: no. of columns, column names
        """

        try:
            json_file = open("schema_training.json", 'r')
            d = json.load(json_file)
            json_file.close()
            col_no = d['NumberofColumns']
            col_names = d['colName'].keys()
            col_names = list(col_names)
            col_info = d['colName']
            logger.info("Obtained info from .json file")
            return col_no, col_names, col_info
        except Exception as e:
            logger.error("Error in obtaining .json file : e: {} ".format(e) )
            raise e


    def create_training_directory(self):
        """"
        Description: Delete Training batches directory, if exist, else  create new directories
               Training_batches/Good_data ->>For validated files
               Training_batches/Bad_data ->>For non validated files

        Input: None
        Output: None
        """
        try:

            if os.path.isdir('Training_batches'):  #Check existing directory
                shutil.rmtree('Training_batches')
                logger.info("Directory Already exists!!! Removed the diretory")
                os.makedirs('Training_batches/Good_data')  # Creating new directory
                os.makedirs('Training_batches/Bad_data')
                logger.info("New directory created at {}".format(os.path.join('.', 'Training_batches\Good_data')))

            else:
                os.makedirs('Training_batches/Good_data') # Creating new directory
                os.makedirs('Training_batches/Bad_data')
                logger.info("New Directory created {}".format(os.path.join('.', 'Training_batches/Good_data')))

        except Exception as e:
            logger.error("Error in Creating  directory : e: {} ".format(e))
            raise e

    def col_length_validation(self, col_no):
        """"
        Description: Check the column length of raw data. If equal to "col_no" move the file to
              'Training_batches/Good_data' , else, move to 'Training_batches/Bad_data'

        Input: col_no
        Output: None
        """
        try:
            for file in os.listdir(self.file_path):
                if file.split('.')[1] == 'csv':
                    data = pd.read_csv(os.path.join(self.file_path, file), header=None)
                    if data.shape[1] == col_no:
                        shutil.copy(os.path.join(self.file_path, file), 'Training_batches/Good_data')
                        logger.info(" {} -Col. length validation completed->>Moved to Good_data Folder".format(file))
                    else:
                        shutil.copy(os.path.join(self.file_path, file), 'Training_batches/Bad_data')
                        logger.info("{} -Col. length Invalid->>Moved to Bad_data Folder : col_length{}".format(file, data.shape[1]))
        except Exception as e:
            logger.error("Error in col length validations : e: {} ".format(e))
            raise e

    def missing_value_validation(self):
        """"
        Description: Used to check missing values in the column. If there is no missing values move the file to
        Good_data folder , else to bad data folder
        """
        try:
            for file in os.listdir('Training_batches/Good_data'):
                data = pd.read_csv(os.path.join('Training_batches/Good_data', file), header=None)
                if data.isna().sum().sum() != 0:
                    shutil.move(os.path.join('Training_batches/Good_data', file)   #move null value files from Good_Data to
                                , os.path.join('Training_batches/Bad_data', file))  # Bad_data folder
                    temp = data.isna().sum()
                    message = "Null values in {} at cols {}".format(file, list(temp[temp != 0].index))
                    logger.info(message + " Data moved to Bad_data folder")
                else:
                    logger.info("No null values in {}, Data Retained".format(file))
            logger.info("COMPLETED VALIDATIONS")

        except Exception as e:
            logger.error("Error in Missing Value Validations : e: {} ".format(e))
            raise e












