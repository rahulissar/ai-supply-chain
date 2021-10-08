######## This module contains all the functions/operation related to data loading ##########

# Importing necessary libraries
import pandas as pd
import os
from pathlib import Path

# Function to read file/folder paths
def get_configuration_file(filename:str=None)->dict:
    try:
        for root,dirs,files in os.walk(os.getcwd()):
            for file in files:
                if file == filename:
                    path = os.path.join(root,file)
        
        # Initialize empty dictionary
        configuration_dict = {}
        with open(path) as f:
            for line in f:
                (key,value) = line.split("=")
                value = value.strip()
                configuration_dict[key.strip()] = value
        return configuration_dict
    except Exception as e:
        return print(e)

# Function to read source data file
def read_source_data(filepath:str=None)->pd.DataFrame:
    # Generate source path
    application_directory = str(Path(os.getcwd()).parent)
    source_file_path = application_directory + filepath
    try:
        # Initialize empty list
        data=[]
        for file_name in os.listdir(source_file_path):
            if file_name.lower().endswith(".csv"):
                data.append(pd.read_csv(os.path.join(source_file_path,file_name),
                encoding='ISO-8859-1'))
            elif file_name.lower().endswith(".xlsx"):
                data.append(pd.read_excel(os.path.join(source_file_path,file_name)))
        return pd.concat(data)
    except Exception as e:
        return print(e)

# list(get_configuration_file(filename='Filepath_configs.txt').values())[0]

# read_source_data(filepath=list(get_configuration_file(filename='Filepath_configs.txt').values())[0])

