import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from wordcloud import WordCloud

from string import punctuation
from sklearn.feature_extraction import stop_words
stopwords = stop_words.ENGLISH_STOP_WORDS
from pipeline_text import *

def convert_series_to_list(df, col):
    return df[col].tolist()

def create_tf_count_vectorizer(docs, stopwords, min_word_count):
    cv = CountVectorizer(docs,stop_words=stopwords,min_df=min_word_count)
    count_vector = cv.fit_transform(docs)
    # count_vector.shape
    return count_vector

def compute_idf_values(word_count_vector):
    tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    return tfidf_transformer

def compute_tf_idf_scores(transformer, count_vector):
    # word counts for the docs - sparse matrix form
    count_vector = cv.transform(docs)
    # compute tf-idf scores
    tf_idf_vector=tfidf_transformer.transform(count_vector)
    
def create_word_cloud_string(df, col, word_cloud_size = 200, score_scale = 1000):
    word_cloud_string = ""
    word_cloud_size = 200
    scale = 1000
    for word in range(word_cloud_size):
        num_occ = int(round(ranked_word_list[f"tfidf-{type_list[type_id]}"][word_cloud_size] * scale))
        word_cloud_string += ((ranked_word_list['index'][word] + " ") * num_occ)
    return word_cloud_string
        
def create_word_cloud(word_cloud_string):
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white',
                collocations=False,
                min_font_size = 10).generate(word_cloud_string) 
                    
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()



if __name__ == "__main__":
    df_raw = pd.read_csv('../data/mbti_1.csv')
    df_user_posts_merged = merge_user_posts_into_string(df_raw, 'posts', delim = "\|\|\|")
    df_type_posts_grouped = group_type_posts(df_user_posts_merged, 'type', 'posts')
    
    type_list = convert_series_to_list(df_type_posts_grouped, 'type')
    docs = convert_series_to_list(df_type_posts_grouped, 'posts')
    
    # tf-idf Calculations
    word_count_vector = create_count_vectorizer(docs, stopwords_set, min_word_count=2)
    tfidf_transformer = compute_idf_values(word_count_vector)
    
    # Word Cloud image creator
    word_cloud_string = create_word_cloud_string(ranked_word_list, f"tfidf-{type_list[type_id]}", word_cloud_size = 200, score_scale = 1000)
    create_word_cloud(word_cloud_string)