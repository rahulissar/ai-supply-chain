import pandas as pd
import numpy as np
from Settings import services_keywords_list
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
from collections import Counter

# Function to identify goods/services from text. Provide input as dataframe & column name
def gen_itemtype(dataframe, column_name, services_keywords_list):
    final_list = '|'.join(services_keywords_list)
    dataframe['Is_Service']=pd.np.where(dataframe[column_name].str.contains(final_list, case=True),1,0)
    return dataframe

# Function to aggregate spend. Provide input as dataframe & list of columns
def spend_agg(dataframe, columns, percentage):
    try:
        aggregated_spend=pd.DataFrame(dataframe.groupby(columns)['Total Price'].agg(['sum','count']).reset_index())
    except Exception as e:
        return print(e)
    else:
        # Sort df by count
        aggregated_spend = aggregated_spend.sort_values(by=('count'), ascending = False)
        # Creating a column for cummaltive amount of rows
        aggregated_spend['cum_sum_count'] = aggregated_spend['count'].cumsum()
        # Creating a column for cummaltive percent of rows
        aggregated_spend['cum_perc_count'] = round(100*aggregated_spend['cum_sum_count']/aggregated_spend['count'].sum(),1)
        # Creating a column for cummaltive sum of total spend
        aggregated_spend['cum_sum_sum'] = aggregated_spend['sum'].cumsum()
        # Creating a column for cummaltive percent of total spend
        aggregated_spend['cum_perc_sum'] = round(100*aggregated_spend['cum_sum_sum']/aggregated_spend['sum'].sum(),1)       
        # Spend Segregator to segregate strategic & tail spend
        aggregated_spend['spend_type'] = np.where((aggregated_spend['cum_perc_count']>float(percentage)), 'Tail Spend', 'Strategic Spend') 
    return aggregated_spend

# Function to merge dataframes
def df_merger(df_left, df_right, how, on):
    final=df_left.merge(df_right, how=how, on=on)
    return final

# Function to group bottom 20% of spend. Must use df from spend aggregator function
def spend_grouper(dataframe, percentage):
    dataframe['Final Category']= np.where((dataframe['cum_perc_count']>float(percentage)) & (dataframe['Is_Service'] == 1), 'Other Services',
                                        np.where((dataframe['cum_perc_count']>float(percentage)) & (dataframe['Is_Service'] == 0), 'Other Goods',
                                        dataframe['Segment Target']))
    return dataframe

# Function to generate similarity matrix. Provide input as df['Column Name'] to this function
def fuzz_similarity(column):
  similarity_array = np.ones((len(column), (len(column))))*100
  for i in range(1, len(column)):
    for j in range(i):
      s1 = fuzz.token_set_ratio(column[i],column[j]) + 0.00000000001
      s2 = fuzz.partial_ratio(column[i],column[j]) + 0.00000000001
      similarity_array[i][j] = 2*s1*s2 / (s1+s2)
      
  for i in range(len(column)):
    for j in range(i+1,len(column)):
      similarity_array[i][j] = similarity_array[j][i]
      np.fill_diagonal(similarity_array, 100)
  return similarity_array

# Function to standardize vendor names. Provide input as dataframe to this function
def standard_name(df_clusters):
  d_standard_name = {}
  for cluster in df_clusters.Cluster.unique():
    names = df_clusters[df_clusters['Cluster']==cluster].Cleaned_Name.to_list()
    l_common_substring = []
    if len(names)>1:
      for i in range(0, len(names)):
        for j in range(i+1, len(names)):
          seqMatch = SequenceMatcher (None, names[i],names[j])
          match = seqMatch.find_longest_match(0, len(names[i]), 0, len(names[j]))
          if (match.size!=0):
            l_common_substring.append(names[i][match.a: match.a + match.size].strip())

      #n = len(l_common_substring)
      counts = Counter(l_common_substring)
      get_mode = dict(counts)
      mode = [k for k, v in get_mode.items() if v == max(list(counts.values()))]
      d_standard_name[cluster] = ";".join(mode)
    else:
      d_standard_name[cluster] = names[0]

  df_standard_names = pd.DataFrame((list(d_standard_name.items())), columns=['Cluster', 'StandardName'])
  df_clusters = df_clusters.merge(df_standard_names, on='Cluster', how='left')
  df_clusters['Score_with_standard'] = df_clusters.apply(lambda x: fuzz.token_set_ratio(x['StandardName' ],x['Cleaned_Name']),axis=1)
  df_clusters['standard_name_withoutSpaces'] = df_clusters.StandardName.apply(lambda x: x.replace(" ",""))
  for name in df_clusters.standard_name_withoutSpaces.unique():
    if len(df_clusters[df_clusters.standard_name_withoutSpaces==name].Cluster.unique()) > 1:
      df_clusters.loc[df_clusters.standard_name_withoutSpaces==name, 'StandardName'] = name
  return df_clusters.drop('standard_name_withoutSpaces', axis=1)