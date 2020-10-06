# Importing the necessary libraries
from sklearn.cluster import AffinityPropagation
import pandas as pd
from Feature_engg import df_merger

def company_clusters(dataframe, matrix):
    cust_ids = dataframe['Supplier Code'].to_list()
    clusters = AffinityPropagation(affinity='precomputed').fit_predict(matrix)
    df_clusters = pd.DataFrame(list(zip(cust_ids, clusters)), columns=['Supplier Code','Cluster'])
    new = df_merger(dataframe, df_clusters, 'inner', 'Supplier Code')
    return new