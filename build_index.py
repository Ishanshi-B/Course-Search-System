#####
# Name: build_index.py
# Date: 2/23/2026
# Description: This is us building the embedding index for each course gets turned into a vector, and your query gets turned into a vector — then you find the closest matches. 
#####

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle

# Load the courses data from the JSON file
with open("courses.json", "r") as file:
    courses = json.load(file)


#Load a free local embedding model from sentence-transformers library
# if we were to deploy this project for a bigger system we could use Vertex AI's text embeddings which would be more powerful and scalable, but for this project we can use a local model to keep it simple and self-contained.
