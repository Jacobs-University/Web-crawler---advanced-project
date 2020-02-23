import pandas as pd
import requests
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def create_vocab_wordCount(list_words):
    stopWordsList=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','can','will','just','don','should','now']
    cv=CountVectorizer(max_df=0.85,stop_words=stopWordsList,max_features=10000)
    word_count_vec=cv.fit_transform(list_words)
    #print (word_count_vector.shape)  #60140 documents in dataset, vocab size is 4734
    print(list(cv.vocabulary_.keys())[:10])
    #return
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vec)
    
    feature_names=cv.get_feature_names()
    #print (feature_names)
    #sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    #print (tfidf_transformer.idf_)
    print (keywords)

def preprocess(web_address,word):
    for address,w in zip(web_address,word):
        url=address
        web=requests.get(url)
        web=re.sub("</?.*?>","<>",web.text)
        web=re.sub("(\\d|\\W)+"," ",web)
        list_words=web.split(" ")
        #return list_words
        create_vocab_wordCount(list_words)
           
data=pd.read_excel('latestResult.xlsx',sheet_name='Websites_top_freq')
#print (data.head)
web_address=data['Website']
word=data['Item']
list_words=preprocess(web_address,word)