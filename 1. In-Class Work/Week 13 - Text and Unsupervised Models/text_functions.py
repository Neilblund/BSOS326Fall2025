import numpy as np
import pandas as pd
import math
def calcKeyness(X, targets, minimum_threshold = 50, feature_names = None):
    """Calculates a keyness statistic for terms in a term-document matrix. 
    X should sparse matrix from CountVectorizer. Y should be a list of True False values"""
    target =  np.array(X[np.where(targets == True)].sum(axis=0)).flatten()
    baseline =  np.array(X[np.where(targets == False)].sum(axis=0)).flatten()
    keyness = []
    target_total = sum(target)
    baseline_total  =sum(baseline)
    norm = 1/ (baseline_total + target_total)
    for i in range(target.size):
        if feature_names is not None:
            term = feature_names[i]
        else:
            term = i
        target_count = target[i] if target[i] > 0 else norm
        baseline_count = baseline[i] if baseline[i] > 0 else norm
        if (baseline_count + target_count) < minimum_threshold: 
                continue
        target_prop = (target_count/target_total)
        baseline_prop = (baseline_count/baseline_total)
        stats = {'term': term,
                 'count_target' : int(target_count),
                 'count_baseline': int(baseline_count),
                 'oddsratio': math.log2( target_prop/baseline_prop)}
        keyness.append(stats)
    return pd.DataFrame(keyness).sort_values('oddsratio')

def getTopicTerms(lda, features, n_terms = 10):
    ls_keywords = []
    ls_freqs = []
    topic_id = []
        
    for i,topic in enumerate(lda.components_):
         # Sorting and finding top keywords
        word_idx = np.argsort(topic)[::-1][:n_terms]
        freqs = list(np.sort(topic)[::-1][:n_terms])
        keywords = [features[i] for i in word_idx]
            
            # Saving keywords and frequencies for later
        ls_keywords = ls_keywords + keywords
        ls_freqs = ls_freqs + freqs
        topic_id = topic_id + [i] * n_terms
            
        
            # Printing top keywords for each topic
        print(i, ', '.join(keywords))
    top_words_df = pd.DataFrame({'keywords':ls_keywords, 'frequency':ls_freqs, 'topic':topic_id})
    return top_words_df

def getTopicDocs(doctopics, n_docs=3, docnames=None):
    """
    Creates a Data Frame with the top n documents for each topic
    """
    if docnames is None:
        docnames = ['doc_'+str(i) for i in range(doctopics.shape[0])]
        
    ls_docs  = []
    ls_probs = []
    topic_id = []

    for i, topic in enumerate(np.transpose(doctopics)):
        # Sorting and finding top keywords
            doc_idx = np.argsort(topic)[::-1][:n_docs]
            probs = list(np.sort(topic)[::-1][:n_docs])
            top_documents = [docnames[i] for i in doc_idx]
    
            ls_docs = ls_docs + top_documents
            ls_probs = ls_probs + probs
            topic_id = topic_id + [i+1] * n_docs

            
    return pd.DataFrame({'documents':ls_docs, 'proportion':ls_probs, 'topic_id':topic_id})
