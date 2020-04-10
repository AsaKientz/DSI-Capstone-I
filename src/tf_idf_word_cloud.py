import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from wordcloud import WordCloud
from pipeline_text import *

custom_stopwords = set("like just people don really ve http com make good things https say way going \
                        lot thing best www youtube ll pretty sure yes no actually right said thanks person \
                        watch did said does maybe probably type types doesn work life want need didn mean \
                        yeah usually got look use day long years year think know feel love friend friends \
                        thinking thought thread post personality mbti try entjs intjs enfps enfjs oh entps \
                        esfjs estjs dont espts im let time infjs infps quite makes little intps isfjs istps \
                        jpg guy guys".split())

stopwords_set = stopwords | custom_stopwords

def convert_series_to_list(df, col):
    return df[col].tolist()

def create_tf_count_vectorizer(docs, stopwords, min_word_count):
    cv = CountVectorizer(docs,stop_words=stopwords,min_df=min_word_count)
    count_vector = cv.fit_transform(docs)
    # count_vector.shape
    return count_vector, cv

def compute_idf_values(word_count_vector):
    tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    return tfidf_transformer

def compute_tf_idf_scores(transformer, count_vector):
    tf_idf_vector = transformer.transform(count_vector)
    return tf_idf_vector

def create_ranked_word_list(cv, tf_idf_vector, type_id, col):
    feature_names = cv.get_feature_names()
    # get tfidf vector for first document
    document_vector = tf_idf_vector[type_id]
    # print the scores
    df = pd.DataFrame(document_vector.T.todense(), index=feature_names, columns=[col])
    ranked_word_list = df.sort_values(by=[col],ascending=False).reset_index()
    return ranked_word_list
    
def create_word_cloud_string(df, col, word_cloud_size = 200, score_scale = 1000):
    word_cloud_string = ""
    word_cloud_size = 200
    scale = 1000
    for word in range(word_cloud_size):
        num_occ = int(round(df[col][word] * scale))
        word_cloud_string += ((df['index'][word] + " ") * num_occ)
    return word_cloud_string
        
def create_word_cloud(word_cloud_string, stopwords, current_type):
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white',
                stopwords = stopwords,
                collocations=False,
                min_font_size = 10).generate(word_cloud_string) 
                    
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    # plt.show()
    plt.savefig(f"images/word_cloud_{current_type}.png")

def word_cloud_generator(df_raw, current_type):
    """
    Main function to convert a raw csv file to a word cloud by way of string and dataframe manipulation,
    tf-idf processing, and would cloud graphics generation.
    INPUT are a raw .csv file of the expected format and the Myers-Briggs Type of interest.
    OUTPUT is a word cloud image.
    """
    df_user_posts_merged = merge_user_posts_into_string(df_raw, 'posts', delim = "\|\|\|")
    df_type_posts_grouped = group_type_posts(df_user_posts_merged, 'type', 'posts')
    # Generate lists
    type_list = convert_series_to_list(df_type_posts_grouped, 'type')
    docs = convert_series_to_list(df_type_posts_grouped, 'posts')
    # tf-idf Calculations
    word_count_vector, cv = create_tf_count_vectorizer(docs, stopwords_set, min_word_count=2)
    tfidf_transformer = compute_idf_values(word_count_vector)
    tf_idf_vector = compute_tf_idf_scores(tfidf_transformer, word_count_vector)
    ranked_word_list = create_ranked_word_list(cv, tf_idf_vector, type_list.index(current_type), f"tfidf-{current_type}")
    # Word Cloud image creator
    word_cloud_string = create_word_cloud_string(ranked_word_list, f"tfidf-{current_type}", word_cloud_size = 200, score_scale = 1000)
    create_word_cloud(word_cloud_string, stopwords_set, current_type)


if __name__ == "__main__":
      
    df_raw = pd.read_csv('data/mbti_1.csv')
    mbti_types = ['ISTJ','ISFJ','INFJ','INTJ', 'ISTP','ISFP','INFP','INTP',
                  'ESTP','ESFP','ENFP','ENTP', 'ESTJ','ESFJ','ENFJ','ENTJ']
    for current_type in range(len(mbti_types)):
        word_cloud_generator(df_raw, mbti_types[current_type])