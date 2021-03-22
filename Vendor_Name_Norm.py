# Importing the necessary libraries
import pandas as pd
import numpy as np
from Data_preprocessing import read_data, pre_processing, preprocess_text
from Settings import column_list, pricing_columns, primary_keys, vendor
from Feature_engg import spend_agg, standard_name, fuzz_similarity
from Clustering import company_clusters
import time

# Function to cluster and process vendor data
def vendor_clustering(dataframe):
    # Select required input
        suppliers = dataframe[['Supplier Code', 'Supplier Name']]
        # pre-process textual data
        suppliers['Cleaned_Name'] = preprocess_text(suppliers['Supplier Name'], eng=False)
        # reset index
        suppliers.reset_index(inplace=True,drop=True)
        # Generate similarity matrix
        print('Approx. time to generate similarity matrix is 20 mins for 3000+ records')
        start_time=time.time()
        print('Matrix Generation started at :',start_time)
        sim=fuzz_similarity(suppliers.Cleaned_Name)
        time.sleep(1)
        end=time.time()
        # total time taken
        print(f"Runtime of the program is {end - start_time}")
        # Start clustering of vendor names
        print('Approx. time to cluster vendor data is 10 mins for 3000+ records')
        start=time.time()
        clustered_vendor=company_clusters(suppliers, sim)
        time.sleep(1)
        end=time.time()
        # total time taken
        print(f"Runtime of the program is {end - start}")
        # Generate standardized names
        final=standard_name(clustered_vendor)
        current_time=time.strftime("%Y%m%d-%H%M%S")
        filename='Vendor_Name_Norm'+str(current_time)+'.csv'
        return final.to_csv(filename)

def run_program(custom=False):
    if custom == False:
        # Read data
        df = read_data('podata.csv')
        # Non-textual data cleansing
        df_cleaned = pre_processing(df, column_list, pricing_columns, primary_keys)
        # Feature engg. through spend aggregation
        df_agg = spend_agg(df_cleaned, vendor, 80.5)
        # Select top spend suppliers
        suppliers = df_agg[df_agg['spend_type'] == 'Strategic Spend']
        vendor_clustering(suppliers)
    else:
        # Read data
        df = read_data('vendor_data.csv')
        # Run clustering algo
        vendor_clustering(df)

if __name__ == '__main__':
	run_program(custom=True)