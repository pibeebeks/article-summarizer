#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:03:58 2019

@author: lumi
"""

#import the libraries
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

#Generate clean sentences. read the article, split into sentences and remove stop words

def read_article(file_name):
#read the file and split each word into article
    doc = open(file_name, 'r')
    doc_data = doc.readlines()
    article = doc_data[0].split(" . ")
    sentences = []
    
# append each word to sentences
    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()

    return sentences

# finding similarity among sentences with the similarity model using cosine similarity
def build_similarity_model(sentence1,sentence2,stopwords=None):
    #create an empty similarity matrix
    if stopwords is None:
        stopwords = []
        
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]
    
    total_words = list(set(sentence1 + sentence2))
    
    vector1 = [0] * len(total_words)
    vector2 = [0] * len(total_words)
    
    #build a vector for the first sentence
    
    for word in sentence1:
        if word in stopwords:
            continue
        vector1[total_words.index(word)] += 1
    #build the vector for the second sentence
    
    for word in sentence2:
        if word in stopwords:
            continue
    vector2[total_words.index(word)] += 1
    
    return 1 - cosine_distance(vector1, vector2)

#build a similarity matrix
def similarity_matrix(sentences, stop_words):
    #create an empty matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  #ignores if they are the same sentence
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1],sentences[idx2], stop_words)
    return similarity_matrix


#generate a summary
def get_summary(file_name , top_n=5):
    stop_words = stopwords.words('english')
    summarise_text = []
    
    #read text and split it 
    sentences = read_article(file_name)
    
    #generate similarity model across sentences
    sentence_similarity_matrix = similarity_matrix(sentences, stop_words)
    
    #rank the sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    
    #sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    print("Indexes of top ranked sentences are order are ", ranked_sentence)
    
    for i in range(top_n):
        summarise_text.append(" ".join(ranked_sentence[i][1]))
        
    #output the summarise text
    print("Summarise text: \n",".".join(summarise_text))
    


#To test call 
    get_summary(file_name, 2)
    
    
    
    
