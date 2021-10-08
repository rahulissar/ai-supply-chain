# Importing the necessary libraries
from data_loader import read_source_data,get_configuration_file
from data_engineering import gen_time_dimensions, aggregate_data
from data_export import export_corr_plot,export_data
import traceback
import logging

def feature_engg():
    try:     
        # Load dimensions
        time_dim = list(get_configuration_file(
            filename='Dimension_configs.txt').values())[0]
        main_dim = list(get_configuration_file(
            filename='Dimension_configs.txt').values())[1].split(',')

        # Load the dataset
        data = read_source_data(filepath=list(get_configuration_file(
            filename='Filepath_configs.txt').values())[0])

        # Create time features
        data = gen_time_dimensions(dataframe=data,time_dimension=time_dim)

        # Aggregate data by main dimensions
        data = aggregate_data(dataframe=data,aggregate_by=main_dim,
        feature_name='avg_sales_main',value_column='sales',aggregation_func='mean')
        # Aggregate data at sku level only
        data = aggregate_data(dataframe=data,aggregate_by=main_dim[0],
        feature_name='avg_sales_sku',value_column='sales',aggregation_func='mean')
        # Aggregate data at store level only
        data = aggregate_data(dataframe=data,aggregate_by=main_dim[1],
        feature_name='avg_sales_store',value_column='sales',aggregation_func='mean')
        # Aggregate the data with time dimensions
        data = aggregate_data(dataframe=data,aggregate_by=main_dim+['dayofweek'],
        feature_name='avg_daily',value_column='sales',aggregation_func='mean')
        data = aggregate_data(dataframe=data,aggregate_by=main_dim+['month'],
        feature_name='avg_monthly',value_column='sales',aggregation_func='mean')
        # Create Rolling Avgs
        rolling_10 = data.groupby(['item'])['sales'].rolling(10).mean().reset_index().drop('level_1',
        axis=1)
        data['rolling_mean_10'] = rolling_10['sales']
        data['rolling_mean_90'] = data.groupby(['item'])['rolling_mean_10'].shift(90)

        # Export Graph
        export_corr_plot(dataframe=data.corr(),filepath=list(get_configuration_file(
            filename='Filepath_configs.txt').values())[1])

        # Export Features
        export_data(dataframe=data,filepath=list(get_configuration_file(
            filename='Filepath_configs.txt').values())[2],
            format='.csv',filename='signal_data')
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        full_trace = traceback.format_exc()
        logging.basicConfig(filename="Data_Export_Log.txt",
                format='%(levelname)s: %(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S') #getLogger()
        logging.exception(message)
        logging.exception(full_trace)
        return print(message)

if __name__ == '__main__':
	feature_engg()

