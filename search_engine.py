#####
# Name: search_engine.py
# Date: 2/28/2026
# Description: This file contains the main search engine logic that takes a user query, parses it for intent, generates embeddings for the query, and retrieves the most relevant courses from the pre-built index. It combines the functionalities of query parsing, embedding generation, and index searching to provide a seamless search experience.
#####

import json
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from query_parser import parse_query_intent

#load everything once at startup to avoid reloading for every query
index = faiss.read_index("courses.index") #loading the pre-built Faiss index from the file
with open("courses_data.pkl", "rb") as f:
    courses = pickle.load(f) #loading the original courses data from the pickle file for later retrieval when we get search results from the index
modal = SentenceTransformer("all-MiniLM-L6-v2") #loading the same embedding model used to build the index for generating query embeddings

#function to search for courses based on a user query
#the top k parameter controls how many results to retrieve from the index, and final_k controls how many results to return after applying any filters based on the parsed query intent.
def search(query: str, top_k: int =  20, final_k: int = 5) -> list: 
    #parse the query to extract structured intent
    intent = parse_query_intent(query) #parsing the user query to extract structured intent

    #embed the query using the same embedding model used to build the index
    query_vec = modal.encode([query]).astype("float32") #generating an embedding for the user query using the loaded embedding model and converting it to float32 for compatibility with the Faiss index
    faiss.normalize_L2(query_vec) #normalizing the query embedding to unit vector for cosine similarity search

    #vector search in the Faiss index to find the top k most similar courses based on the query embedding
    scores, indices = index.search(query_vec, top_k) #searching the Faiss index for the top k most similar courses based on the query embedding and retrieving their scores and indices
    #the candidates vairable is a list of tuples where each tuple contains a course dictionary and its corresponding similarity score. The courses are retrieved from the original courses data using the indices returned by the Faiss index search.
    candidates = [(courses[i], float(scores[0][j]))
                  for j,i in enumerate(indices[0])] 
    
    #apply the hard filters based on the intent
    filtered_candidates = []
    for course, score in candidates:
        if intent["max_duration"] and course["duration_minutes"] > intent["max_duration"]:
            continue
        if intent["preferred_format"] and course["format"] != intent["preferred_format"]:
            score *= 0.7 #soft penalty for format mismatch
        if intent["preferred_level"] and course["level"] != intent["preferred_level"]:
            score *= 0.85 #penalty for level mismatch
        filtered_candidates.append((course, score))

    # re rank and return the top results based on the adjusted scores after applying the filters. 
    # The results are sorted in descending order of their scores, and only the top final_k results are returned to the user.
    filtered_candidates.sort(key=lambda x: x[1], reverse=True)
   
    return {
        "intent": intent,
        "results": filtered_candidates[:final_k]
    }