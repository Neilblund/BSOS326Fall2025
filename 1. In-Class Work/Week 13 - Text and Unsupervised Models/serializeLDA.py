# Example of storing an LDA pipeline as a pickle so it can be re-used

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing

import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk import SnowballStemmer
from sklearn.decomposition import LatentDirichletAllocation
import pickle


articles = pd.read_csv('https://github.com/Neilblund/APAN/raw/main/news_sample.csv')




eng_stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return [stemmer.stem(token).lower() for token in tokens if token not in eng_stopwords and token.isalpha()]
vectorizer = CountVectorizer(analyzer = 'word',
                             ngram_range=(0,1), # Tokens are individual words for now
                             strip_accents='unicode',
                             max_df = 0.1, # maximum number of documents in which word j occurs. 
                             min_df = .0025 # minimum number of documents in which word j occurs. 
                            )

lda_pipeline = Pipeline([('vectorizer', 
                          vectorizer), 
                         ('lda',
                          LatentDirichletAllocation(n_components = 15, # number of topics. Try different numbers here to see what works best. Usually somewhere between 20 - 100
                                                    random_state = 123, # random number seed. You can use any number here, but its important to include so you can replicate analysis
                                                    doc_topic_prior = 1/15) 
)])


# fitting the model to the articles
lda_pipeline.fit(articles['text'])
with open('newstopics15.pickle', 'wb') as file:
    # Use pickle.dump() to serialize the 'data' object and write it to the file
    pickle.dump(lda_pipeline, file)
