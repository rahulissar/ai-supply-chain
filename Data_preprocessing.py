import pandas as pd
import unicodedata
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
import nltk
from Settings import vendor_stopwords, max_length
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from gensim.models.word2vec import Word2Vec
from gensim.models.phrases import Phrases, Phraser

# Importing the dataframe function
def read_data(URL):
    try:
        return pd.read_csv(URL)
    except Exception as e:
        return print(e)
    #return pd.read_csv(URL)

# Data pre-processing function for reducing dimensions & cleaning pricing data
def pre_processing(df, column_list, pricing_columns, primary_keys):
    try:
        df_new = df[column_list]
    except KeyError as E1:
        print('Invalid Column Name Provided', E1)
    # Dropping Null Values
    df_new.dropna(inplace=True)
    # Changing the data types
    for y in primary_keys:
        try:
            df_new[y] = df_new[y].astype(int)
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
            print('Data could not be converted into float', V2)
    # Dropping duplicate values in dataframe
    df_new.drop_duplicates(inplace=True)
    # Dropping negative invoice values in dataframe
    df_new.drop(df_new[df_new['Total Price'] <= 0].index, inplace=True)
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

# Trim the text to remove tabs, linebreaks, double spaces
def clean_spaces(text):
    text=re.sub(r'\s+', ' ', text)
    text=text.strip()
    if len(text) < 1:
        text=''
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
        vec = CountVectorizer(stop_words=custom,ngram_range=(1,2),min_df=10)
        Vec_X = vec.fit_transform(column)
        return Vec_X
    elif get_features == True and tdfidf == False:
        vec = CountVectorizer(stop_words=custom,ngram_range=(1,2),min_df=10)
        Vec_X = vec.fit_transform(column)
        return vec.get_feature_names()
    elif get_features == False and tdfidf == True:
        tdf = TfidfVectorizer(stop_words=custom,ngram_range=(1,2),min_df=10)
        tdf_X = tdf.fit_transform(column)
        return tdf_X
    elif get_features == True and tdfidf == True:
        tdf = TfidfVectorizer(stop_words=custom,ngram_range=(1,2),min_df=10)
        tdf_X = tdf.fit_transform(column)
        return tdf.get_feature_names()

# Function to extract corpus of words (unigrams only) from text column. Provide input as df['Column Name'] to this function
def extract_corpus(column):
    try:
        corpus = column
    except Exception as e:
        return print(e)
    ## create empty list of lists of unigrams
    lst_corpus = []
    try:
        for string in corpus:
            lst_words = string.split()
            lst_grams = [" ".join(lst_words[i:i+1]) for i in range(0, len(lst_words), 1)]
            lst_corpus.append(lst_grams)
        ## detect bigrams and trigrams
        bigrams_detector = Phrases(lst_corpus, delimiter=" ".encode(), 
                            min_count=10, threshold=10)
        bigrams_detector = Phraser(bigrams_detector)
        trigrams_detector = Phrases(bigrams_detector[lst_corpus], delimiter=" ".encode(), 
                            min_count=15, threshold=10)
        trigrams_detector = Phraser(trigrams_detector)
        ## detect common bigrams and trigrams using the fitted detectors
        lst_corpus = list(bigrams_detector[lst_corpus])
        lst_corpus = list(trigrams_detector[lst_corpus])
        return lst_corpus
    except Exception as e:
        return print(e)

# Function to extract maximum length for padding. Provide input as df['Column Name'] to this function
def extract_maxlength(column):
    try:
        max_length = max([len(s.split()) for s in column])
        return print('Input this length into Settings.py file :', max_length)
    except Exception as e:
        return print(e)

# Function to tokenize textual data and create padded sequences.
def tokenize_text(unigram_list, return_vocab=False):
    tokenizer = Tokenizer(num_words=30000, lower=True, split=' ', oov_token="NaN", filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
    try:
        tokenizer.fit_on_texts(unigram_list)
    except Exception as e:
        return print(e)
    else:
        if return_vocab == False:
            # create sequences
            text_seq = tokenizer.texts_to_sequences(unigram_list)
            # pad sequences
            text_pad = pad_sequences(text_seq, maxlen=max_length, padding='post', truncating='post')
            # create dataframe of padded text
            df = pd.DataFrame(text_pad)
            return df
        else:
            dic_vocabulary = tokenizer.word_index
            return dic_vocabulary

# Function to generate word2vec model
def word2vec_model(unigram_list):
    try:
        # fit w2v
        nlp = Word2Vec(unigram_list, size=100, window=5, workers=4, min_count=25, iter=10)
        return nlp
    except Exception as e:
        return print(e)