from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
#from pipelines.regions_utils import HandRegions
from enum import Enum

class HandRegions(Enum):
    """
    Used as region keys to
    - save and load data
    - in dicts that pass data down the pipelines.
    """

    HAND_0 = "Hand"
    HANDBODY_1 = "HandBody"
    THUMB_2 = "Thumb"
    INDEXFINGER_3 = "IndexFinger"
    MIDDLEFINGER_4 = "MiddleFinger"
    RINGFINGER_5 = "RingFinger"
    LITTLEFINGER_6 = "LittleFinger"

uuid = "uuid1"

embeddings_dict = {
    HandRegions.HAND_0.value: {"Embedding": [0.1]},
    HandRegions.HANDBODY_1.value: {"Embedding": [0.2]},
    HandRegions.THUMB_2.value: {"Embedding": [0.6]},
    HandRegions.INDEXFINGER_3.value: {"Embedding": [0.3]},
    HandRegions.MIDDLEFINGER_4.value: {"Embedding": [0.4]},
    HandRegions.RINGFINGER_5.value: {"Embedding": [0.5]},
    HandRegions.LITTLEFINGER_6.value: {"Embedding": [0.6]},
}

collection_name = "hand_regions"    

top_k = 5

search_params = {
    "metric_type": "L2",           # Gleiche Metrik wie beim Index
    "params": {"nprobe": 10}       # Anzahl der durchsuchten Cluster (abhängig von nlist)
}

###########################################################################


def add_embeddings_to_vectordb(uuid, embeddings_dict, collection_name):

    connect_to_milvus(collection_name)

    milvus_data  = prepare_data_for_milvus(uuid, embeddings_dict)

    add_embeddings(milvus_data, collection_name)

    connections.disconnect("default")


def connect_to_milvus(collection_name):

    connect_to_host()

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="uuid", dtype=DataType.VARCHAR, max_length=36),
        FieldSchema(name="region", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024)
    ] 

    schema = CollectionSchema(fields, description="HandRegions-Embedding")

    if not utility.has_collection(collection_name):
        collection = Collection(name=collection_name, schema=schema)
        print(f"Collection '{collection_name}' successfully created.")

        for region in HandRegions:
            partition_name = region.value
            if not collection.has_partition(partition_name):
                collection.create_partition(partition_name=partition_name)
                print(f"Partition '{partition_name}' successfully created.")
        
        index_params = {
            "index_type": "IVF_FLAT",  # Alternativen: "HNSW", "IVF_SQ8", etc.
            "metric_type": "L2",      # Metrik: L2 (Euclidean Distance), COSINE, oder IP
            "params": {"nlist": 128}  # IVF-Parameter: Anzahl der Cluster
        }
        collection.create_index(field_name="vector", index_params=index_params)

    else:
        collection = Collection(name=collection_name)
        print(f"Collection '{collection_name}' exists.")


def connect_to_host():
    if not connections.has_connection("default"):
        try:
            connections.connect(alias="default", host="localhost", port="19530")
        except Exception as e:
            print(f"Failed to connect to Host: {str(e)}")
            return


def prepare_data_for_milvus(uuid, embeddings_dict):

    uuids = []
    regions = []
    embeddings = []
   
    for region, values in embeddings_dict.items():
        uuids.append(uuid)
        regions.append(region)
        embeddings.append(values["Embedding"])

    return {
        "UUIDS": uuids,
        "Regions": regions,
        "Embeddings": embeddings
    }


def add_embeddings(milvus_data, collection_name):

    collection = Collection(name=collection_name)

    for i in range(len(milvus_data["UUIDS"])):
        region = milvus_data["Regions"][i]
        collection.insert(
            data=[
                [milvus_data["UUIDS"][i]],
                [milvus_data["Regions"][i]],
                [milvus_data["Embeddings"][i]],
            ],
            partition_name=region
        )
    print(f"Successfully added entries to Milvus.")


def query_embeddings_dict(embeddings_dict, collection_name, search_params, top_k):
    
    connect_to_host()

    if not utility.has_collection(collection_name):
        print(f"Collection with name '{collection_name}' not found.")
    else:
        collection = Collection(name=collection_name)

    results_by_region = {}

    for region, values in embeddings_dict.items():
        query_vector = [values["Embedding"]]

        results = collection.search(
            data=query_vector,
            anns_field="vector",
            param=search_params,
            limit=top_k,
            partition_names=[region],
            output_fields=["uuid"]
        )

        results_by_region[region] = []
        for hits in results:
            for hit in hits:
                results_by_region[region].append({
                    "id": hit.id,
                    "uuid": hit.entity.get("uuid"),
                    "distance": hit.distance
                })

    connections.disconnect("default")

    # Aufbau results_by_region (region als Key):
    # results_by_region = {
    # "Thumb": [  
    #     {"id": 1024, "uuid": "uuid1", "distance": 0.123},
    #     {"id": 1023, "uuid": "uuid2", "distance": 0.234},
    #     {"id": 1022, "uuid": "uuid3", "distance": 0.345},
    # ],
    # ...

    return results_by_region  