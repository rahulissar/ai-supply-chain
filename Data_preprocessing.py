import pandas as pd
import unicodedata
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
import nltk
from Settings import vendor_stopwords

# Importing the dataframe function
def read_data(URL):
    return pd.read_csv(URL)

# Data pre-processing function for reducing dimensions & cleaning pricing data
def pre_processing(df, column_list, pricing_columns):
    try:
        df_new = df[column_list]
    except KeyError as E1:
        print('Invalid Column Name Provided', E1)
    # Dropping Null Values
    df_new.dropna(inplace=True)
    # Changing the data types
    try:
        df_new['Supplier Code'] = df_new['Supplier Code'].astype(int)
    except ValueError as V1:
        print('Data could not be converted into integer', V1)
    # Creating for loop to replace spl chars
    for x in pricing_columns:
        try:
            df_new[x] = df_new[x].str.replace(r'[^\d.]+', '')
        except KeyError as E2:
            print('Invalid Column Name Provided', E2)
        try:
            df_new[x] = df_new[x].astype(float)
        except ValueError as V2:
            print('Data could not be converted into integer', V2)
    # Dropping duplicate values in dataframe
    df_new.drop_duplicates(inplace=True)
    # Dropping negative invoice values in dataframe
    df_new[df_new['Total Price'] <= 0].index
    # Resetting the index of the cleaned dataframe
    df_new.reset_index(inplace=True,drop=True)
    return df_new

# Text data encoder function
def filter_ascii(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

# Remove spl characters & digits (optional) function
def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

# Remove vendor specific stop words
def clean_stopwords(text,eng=False):
    if eng == False:
        custom = vendor_stopwords
    else:
        custom = vendor_stopwords + list(ENGLISH_STOP_WORDS)
    for x in custom:
        pattern2 = r'\b'+x+r'\b'
        text=re.sub(pattern2,'',text)
    return text

# Trim the text to remove spaces
def clean_spaces(text):
    text=text.replace('  ', ' ')
    text=text.strip()
    if len(text) < 1:
        text='Tooshorttext'
    return text

# Function to Preprocess Textual data. Provide input as df['Column Name'] to this function
def preprocess_text(column, remove_digits=True, lemm=True, eng=False):
    try:
        column = [filter_ascii(text) for text in column]
        column = [remove_special_characters(text, remove_digits) for text in column]
        column = [text.lower() for text in column]
        column = [clean_stopwords(text, eng) for text in column]
        column = [clean_spaces(text) for text in column]
        ## Lemmatisation (convert the word into root word)
        if lemm == True:
            lem = nltk.stem.wordnet.WordNetLemmatizer()
            column = [lem.lemmatize(text) for text in column]
        return column
    except Exception as e:
        return print(e)

# Function to get the sparse matrix of vectors or features. Provide input as df['Column Name'] to this function
def gen_wordvec(column, get_features=False, tdfidf=False):
    custom = vendor_stopwords + list(ENGLISH_STOP_WORDS)
    if get_features == False and tdfidf == False:
        vec = CountVectorizer(stop_words=custom,ngram_range=(1,2),min_df=2)
        Vec_X = vec.fit_transform(column)
        return Vec_X
    elif get_features == True and tdfidf == False:
        vec = CountVectorizer(stop_words=custom,ngram_range=(1,2),min_df=2)
        Vec_X = vec.fit_transform(column)
        return vec.get_feature_names()
    elif get_features == False and tdfidf == True:
        tdf = TfidfVectorizer(stop_words=custom,ngram_range=(1,2),min_df=2)
        tdf_X = tdf.fit_transform(column)
        return tdf_X
    elif get_features == True and tdfidf == True:
        tdf = TfidfVectorizer(stop_words=custom,ngram_range=(1,2),min_df=2)
        tdf_X = tdf.fit_transform(column)
        return tdf.get_feature_names()
