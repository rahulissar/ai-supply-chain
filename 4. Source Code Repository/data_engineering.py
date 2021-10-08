######## This module contains all the functions/operation related to data engineering ##########

# Importing necessary libraries
import pandas as pd
# import numpy as np

# Function to aggregate the data
def aggregate_data(dataframe:pd.DataFrame=None,aggregate_by:list=None,
feature_name:str=None,value_column:str=None,
aggregation_func:str=None)->pd.DataFrame:
    try:
        new = dataframe.groupby(aggregate_by).agg(value = (value_column,
        aggregation_func)).reset_index()
        new.rename(columns={'value':feature_name},inplace=True)
        return pd.merge(left=dataframe,right=new,on=aggregate_by,how='left')
    except Exception as e:
        return print(e)

# Function to parse time dimension
def gen_time_dimensions(dataframe:pd.DataFrame=None,
time_dimension:str=None)->pd.DataFrame:
    try:
        # Generate date features
        dataframe['date'] = pd.to_datetime(dataframe[time_dimension])
        dataframe['year'] = dataframe.date.dt.year
        dataframe['month'] = dataframe.date.dt.month
        dataframe['day'] = dataframe.date.dt.day
        dataframe['dayofyear'] = dataframe.date.dt.dayofyear
        dataframe['dayofweek'] = dataframe.date.dt.dayofweek
        dataframe['weekofyear'] = dataframe.date.dt.weekofyear
        dataframe["is_wknd"] = dataframe.date.dt.weekday // 4
        dataframe['is_month_start'] = dataframe.date.dt.is_month_start.astype(int)
        dataframe['is_month_end'] = dataframe.date.dt.is_month_end.astype(int) 
        # # Additionnal Data Features
        # dataframe['day^year'] = np.log((np.log(dataframe['dayofyear'] + 1)) ** (dataframe['year'] - 2000))
        return dataframe
    except Exception as e:
        return print(e)