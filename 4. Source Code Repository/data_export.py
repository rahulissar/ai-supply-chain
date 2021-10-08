######## This module contains all the functions/operation related to data exports ##########

# Importing necessary libraries
import pandas as pd
import os
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import time

# Data Visualization & Export
def export_corr_plot(dataframe:pd.DataFrame=None,filepath:str=None):
    try:
        # Generate destination path
        application_directory = str(Path(os.getcwd()).parent)
        destination_file_path = application_directory + filepath

        # Generate plot
        plt.subplots(figsize=(30,30))
        graph = sns.heatmap(data=dataframe.corr(),annot=True)
        file = graph.get_figure()
        file.savefig(destination_file_path+'/Corr_Plot.pdf')
        # plt.figure(figsize=(30,30))
        # plt.savefig(destination_file_path+'/Corr_Plot.pdf')
        return print("Correlation Plot Exported Successfully")
    except Exception as e:
        return print(e)

# Aggregated Features Export
def export_data(dataframe:pd.DataFrame=None,filepath:str=None,
format:str=None,filename:str=None):
    try:
        # Generate timestamp
        now = str(time.strftime('%d-%m-%Y %H:%M:%S'))

        # Generate destination path
        application_directory = str(Path(os.getcwd()).parent)
        destination_file_path = application_directory + filepath + now + filename

        if format != '.csv':
            dataframe.to_pickle(destination_file_path+'.pkl')
            return print("Pickle Exported Successfully")
        else:
            dataframe.to_csv(destination_file_path+format,index=False)
            return print("CSV Exported Successfully")
    except Exception as e:
        return print(e)