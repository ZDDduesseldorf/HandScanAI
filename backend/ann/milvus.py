from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
from typing import Dict, List, Any

# from pipelines.regions_utils import HandRegions
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
    "metric_type": "L2",  # Gleiche Metrik wie beim Index
    "params": {"nprobe": 10},  # Anzahl der durchsuchten Cluster (abhängig von nlist)
}

###########################################################################


def add_embeddings_to_vectordb(uuid: str, embeddings_dict: Dict[str, Dict[str, Any]], collection_name: str) -> None:
    """
    Adds embeddings to the Milvus vector database.

    Args:
        uuid (str): The UUID associated with the embeddings.
        embeddings_dict (Dict[str, Dict[str, Any]]): Dictionary containing regions and their embeddings.
        collection_name (str): Name of the Milvus collection.

    Returns:
        None
    """
    connect_to_milvus(collection_name)

    milvus_data = prepare_data_for_milvus(uuid, embeddings_dict)

    add_embeddings(milvus_data, collection_name)


def connect_to_milvus(collection_name: str) -> None:
    """
    Connects to Milvus and initializes the collection if it does not exist.

    Args:
        collection_name (str): Name of the Milvus collection to connect or create.

    Returns:
        None
    """
    connect_to_host()

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="uuid", dtype=DataType.VARCHAR, max_length=36),
        FieldSchema(name="region", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
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
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128},
        }
        if not collection.has_index():
            collection.create_index(field_name="vector", index_params=index_params)
    else:
        collection = Collection(name=collection_name)
        print(f"Collection '{collection_name}' exists.")


def connect_to_host() -> None:
    """
    Connects to the Milvus host.

    Returns:
        None
    """
    if not connections.has_connection("default"):
        try:
            connections.connect(alias="default", host="localhost", port="19530")
        except Exception as e:
            print(f"Failed to connect to Host: {str(e)}")
            return


def prepare_data_for_milvus(uuid: str, embeddings_dict: Dict[str, Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Prepares data for insertion into Milvus.

    Args:
        uuid (str): The UUID associated with the embeddings.
        embeddings_dict (Dict[str, Dict[str, Any]]): Dictionary containing regions and their embeddings.

    Returns:
        Dict[str, List[Any]]: Prepared data including UUIDs, regions, and embeddings.
    """
    uuids = []
    regions = []
    embeddings = []

    for region, values in embeddings_dict.items():
        uuids.append(uuid)
        regions.append(region)
        embeddings.append(values["Embedding"])

    return {"UUIDS": uuids, "Regions": regions, "Embeddings": embeddings}


def add_embeddings(milvus_data: Dict[str, List[Any]], collection_name: str) -> None:
    """
    Adds prepared embeddings to the specified Milvus collection.

    Args:
        milvus_data (Dict[str, List[Any]]): Prepared data including UUIDs, regions, and embeddings.
        collection_name (str): Name of the Milvus collection.

    Returns:
        None
    """
    collection = Collection(name=collection_name)

    for i in range(len(milvus_data["UUIDS"])):
        region = milvus_data["Regions"][i]

        collection.insert(
            data=[
                [milvus_data["UUIDS"][i]],
                [milvus_data["Regions"][i]],
                [milvus_data["Embeddings"][i]],
            ],
            partition_name=region,
        )
    print("Successfully added entries to Milvus.")


def query_embeddings_dict(
    embeddings_dict: Dict[str, Dict[str, Any]], collection_name: str, search_params: Dict[str, Any], top_k: int
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Queries embeddings in the Milvus vector database.

    Args:
        embeddings_dict (Dict[str, Dict[str, Any]]): Dictionary containing regions and their embeddings.
        collection_name (str): Name of the Milvus collection.
        search_params (Dict[str, Any]): Parameters for the search query.
        top_k (int): Number of nearest neighbors to retrieve.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Query results grouped by region.
    """
    connect_to_host()

    if not utility.has_collection(collection_name):
        print(f"Collection with name '{collection_name}' not found.")
        return {}

    collection = Collection(name=collection_name)
    collection.load()

    results_by_region = {}

    for region, values in embeddings_dict.items():
        query_vector = [values["Embedding"]]

        try:
            results = collection.search(
                data=query_vector,
                anns_field="vector",
                param=search_params,
                limit=top_k,
                partition_names=[region],
                output_fields=["uuid"],
            )

            results_by_region[region] = []
            for hits in results:
                for hit in hits:
                    results_by_region[region].append(
                        {
                            "id": hit.id,
                            "uuid": hit.entity.get("uuid"),
                            "distance": hit.distance,
                        }
                    )
        except Exception as e:
            print(f"Search query failed for region '{region}': {e}")
            results_by_region[region] = []

    collection.release()
    print(f"Collection '{collection_name}' released from memory.")

    return results_by_region
