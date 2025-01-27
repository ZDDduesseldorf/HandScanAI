from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import numpy as np

# Example data
data = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
query = np.array([[1, 3]])
dimension = data.shape[1]

# Connect to Milvus
# Adjust "host" and "port" if your Milvus configuration is different.
connections.connect("default", host="milvus-standalone", port="19530")

# Collection name
collection_name = "example_balltree_equivalent"

# Check if collection exists; if yes, drop it
if collection_name in utility.list_collections():
    existing_collection = Collection(collection_name)
    existing_collection.drop()

# Define a collection schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dimension)
]

schema = CollectionSchema(fields, description="Example collection for vector search")

# Create the collection
collection = Collection(name=collection_name, schema=schema)

# Prepare data for insertion
ids = list(range(len(data)))
entities = [
    ids,  # IDs
    data.tolist()  # Vectors
]

# Insert data into the collection
collection.insert(entities)

# Create an index to speed up similarity search
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 10}
}

collection.create_index(field_name="embeddings", index_params=index_params)
print("Index created successfully.")

# Load the collection into memory for searching
collection.load()

# Prepare query vector in list form
query_vectors = query.tolist()

# Perform similarity search with k=2 (like in BallTree query)
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=query_vectors, 
    anns_field="embeddings", 
    param=search_params, 
    limit=3,
    output_fields=["id"]
)

# Display search results
for i, hits in enumerate(results):
    print(f"Query {i}:")
    for hit in hits:
        print(f"ID: {hit.id}, Distance: {hit.distance}")
    print()

# Disconnect from Milvus server
connections.disconnect("default")