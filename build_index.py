#####
# Name: build_index.py
# Date: 2/23/2026
# Description: This is us building the embedding index for each course gets turned into a vector, and your query gets turned into a vector — then you find the closest matches. 
# Refernces:
# Pickling: https://www.blackduck.com/blog/python-pickling.html#:~:text=Pickle%20in%20Python%20is%20primarily,in%20populating%20the%20object%20structure.
# Faiss: 
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
model = SentenceTransformer("all-MiniLM-L6-v2") # this is a smaller model 

print("Embedding courses...")

# Generate embeddings for each course's searchable text and store them in a list
texts = [c["searchable_text"] for c in courses] #extracting the searchable text from each course to generate embeddings
embeddings = model.encode(texts, show_progress_bar=True) #generating embeddings for the searchable text of each course using the loaded model

# The .astype("float32") converts each number from 64-bit to 32-bit floating point. FAISS specifically requires float32 — if you pass float64 it will throw an error. 
# It also halves the memory usage which matters at scale.
embeddings = np.array(embeddings).astype("float32") 

# Building the Faiss index that is the local vertex ai search
# For a 500×384 grid, .shape returns (500, 384). The [1] grabs the second value — 384 
dimensions = embeddings.shape[1] #getting the number of dimensions of the embeddings to initialize the Faiss index
index = faiss.IndexFlatIP(dimensions) #creating a Faiss index for inner product = cosine similarity if normalized

#Now we normalize for the cosine similarity search

faiss.normalize_L2(embeddings) #normalizing the embeddings to unit vectors for cosine similarity search
index.add(embeddings) #adding the normalized embeddings to the Faiss index

# Save the index to a file
faiss.write_index(index, "courses.index")
with open("courses_data.pkl", "wb") as f:
    pickle.dump(courses, f) #saving the original courses data to a pickle file for later retrieval when we get search results from the index
with open("embedding_model_name.txt", "w") as f:
    f.write("all-MiniLM-L6-v2") #saving the name of the embedding model used to a text file for reference when we need to load the same model for generating query embeddings during search

print (f"Index built with {index.ntotal} vectors of dimension {dimensions}")