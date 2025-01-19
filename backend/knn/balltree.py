from sklearn.neighbors import BallTree
import numpy as np
import joblib
from io import BytesIO

############### Example ######################################################

# Data + Query input
data = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
input = np.array([[1, 3]])

# Example for Ball Tree
bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = bt.query(input, k=2)

print("Ball-Tree")
print(f"Indices: {ind}")
print(f"Distances: {dist}")

############### kNN Implementation ###########################################

# Prepare tree as binary data for mongoDB
def serialize_tree_data(tree, name):
    buffer = BytesIO()
    joblib.dump(tree, buffer)
    buffer.seek(0)

    joblib_data = buffer.read()
    document = {
        "name": f"{name}_balltree",
        "data": joblib_data
    }

    return document

# Restore tree data from mongoDB
def retrieve_tree_data():
    stored_document = "" # collection.find_one({"name": "balltree"}) -> import pymongo first
    retrieved_data = stored_document["data"]
    buffer = BytesIO(retrieved_data)
    loaded_tree = joblib.load(buffer)
    
    return loaded_tree

# Normalize embeddings for cosine-approximation
# normalized_embeddings = normalize(embeddings, norm='l2')

# Ball Trees for all embedding types
hand_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = hand_bt.query(input, k=2)

palm_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = palm_bt.query(input, k=2)

thumb_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = thumb_bt.query(input, k=2)

index_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = index_bt.query(input, k=2)

middle_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = middle_bt.query(input, k=2)

ring_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = ring_bt.query(input, k=2)

pinky_bt =  BallTree(data, leaf_size=10, metric='euclidean')
dist, ind = pinky_bt.query(input, k=2)

print(BallTree.valid_metrics)