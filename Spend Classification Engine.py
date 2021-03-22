# Importing the necessary libraries
import pandas as pd
import numpy as np
import time
from Data_preprocessing import read_data, pre_processing, preprocess_text, gen_wordvec
from Settings import column_list, pricing_columns, primary_keys, category, services_keywords_list, textual_data, target
from Feature_engg import spend_agg, gen_itemtype, spend_grouper, merge_desc, df_merger,  filter_df, train_test, split_variables



# Read data
df = read_data('podata.csv')
# Non-textual data cleansing
df_cleaned = pre_processing(df, column_list, pricing_columns, primary_keys)
# Textual data clensing for supplier name
df_cleaned['supplier_cleaned'] = preprocess_text(df_cleaned['Supplier Name'])
# Textual data clensing for item desc
df_cleaned['item_desc'] = preprocess_text(df_cleaned['Item Description'], eng=True)
# Textual data clensing for item name
df_cleaned['item_name'] = preprocess_text(df_cleaned['Item Name'], eng=True)
# Merge all textual columns
df_cleaned = merge_desc(df_cleaned, textual_data)
# Generate item type according to item descriptions
df_cleaned = gen_itemtype(df_cleaned, 'bow', services_keywords_list)
# Feature engg. through spend aggregation
df_agg = spend_agg(df_cleaned, category, 80.5)
# Generate item type according to item category
df_agg = gen_itemtype(df_agg, 'Segment Title', services_keywords_list)
# Grouping tail spend categories into other goods/services and generate labels
df_agg = spend_grouper(df_agg, 80.5)
# Merging final labels and label codes
df_new = df_merger(df_cleaned, df_agg[target], 'inner', category)
# Split train-test datasets
train, test = train_test(df_new, 0.2)
# Generate word vector
vec_train = gen_wordvec(train['bow'], tdfidf=True)
vec_test = gen_wordvec(test['bow'], tdfidf=True)
# Filter dataframe
train_prefinal = filter_df(train)
test_prefinal = filter_df(test)
# Change dtypes
train = train_prefinal.astype(np.float32)
test = test_prefinal.astype(np.float32)
# Split independent and dependent variables for both train & test sets
train_x, train_y = split_variables(train_prefinal)
test_x, test_y = split_variables(test_prefinal)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=20, max_depth=1000)
model.fit(vec_train, train_y)

from sklearn.model_selection import cross_val_score
# cross-validation score
rd_score = np.mean(cross_val_score(model, vec_train, train_y, cv = 3, n_jobs = -1))

# create dataframe with unique values matching for numeric and string names for segment
df_segment = df_agg[['Final_Category', 'Final_Code']].drop_duplicates()
df_segment
# create a dictionary 
dict_segment = pd.Series(df_segment['Final_Category'].values,index=df_segment['Final_Code']).to_dict()
# create df for categories names based on category number
cat_num = df_segment['Final_Code'].unique()
cat_num = pd.DataFrame(sorted(cat_num), columns=['Final_Code'])
sorted_cat_names = cat_num['Final_Code'].map(dict_segment)
# predict
from sklearn.metrics import classification_report
y_pred = model.predict(vec_test)
print(classification_report(test_y,y_pred, target_names= sorted_cat_names))