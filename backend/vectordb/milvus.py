from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from typing import Dict, List, Any
from utils.key_enums import HandRegions, PipelineDictKeys

import torch

# Global variables

milvus_collection_name = "hand_regions"

milvus_metric_type = "COSINE"

milvus_index_params = {
    "index_type": "FLAT",
    "metric_type": milvus_metric_type,
    "params": {"nlist": 128},
}

milvus_default_search_params = {
    "metric_type": milvus_metric_type,  # Gleiche Metrik wie beim Index
    "params": {"nprobe": 10},  # Anzahl der durchsuchten Cluster (abhängig von nlist)
}

###########################################################################


def add_embeddings_to_milvus(
    uuid: str, embeddings_dict: Dict[str, torch.Tensor], collection_name: str, model_name="DENSENET_121"
) -> bool:
    """
    Adds embeddings to the Milvus vector database.

    Args:
        uuid (str): The UUID associated with the embeddings.
        embeddings_dict (Dict[str, Dict[str, Any]]): Dictionary containing regions and their embeddings.
        collection_name (str): Name of the Milvus collection.

    Returns:
        None
    """
    try:
        connect_to_host()
        create_miluvs_collection(collection_name, model_name)
        milvus_data = prepare_data_for_milvus(uuid, embeddings_dict)
        insert_embeddings(milvus_data, collection_name)
        print("Successfully added embeddings.")
        return True

    except Exception as e:
        print(f"Adding embeddings has failed. An error has occured: {e}")
        return False


def create_miluvs_collection(collection_name: str, model_name="DENSENET_121") -> None:
    """
    Connects to Milvus and initializes the collection if it does not exist.

    Args:
        collection_name (str): Name of the Milvus collection to connect or create.

    Returns:
        None
    """

    fields_dict = {
        "DENSENET_121": [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="uuid", dtype=DataType.VARCHAR, max_length=36),
            FieldSchema(name="region", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
        ],
        "DENSENET_169": [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="uuid", dtype=DataType.VARCHAR, max_length=36),
            FieldSchema(name="region", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1664),
        ],
        "RESNET_50": [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="uuid", dtype=DataType.VARCHAR, max_length=36),
            FieldSchema(name="region", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1000),
        ],
    }

    schema = CollectionSchema(fields=fields_dict[model_name], description="HandRegions-Embedding")

    if not utility.has_collection(collection_name):
        collection = Collection(name=collection_name, schema=schema)
        print(f"Collection '{collection_name}' successfully created.")

        for region in HandRegions:
            partition_name = region.value
            if not collection.has_partition(partition_name):
                collection.create_partition(partition_name=partition_name)
                print(f"Partition '{partition_name}' successfully created.")

        if not collection.has_index():
            collection.create_index(field_name="vector", index_params=milvus_index_params)
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
            connections.connect(alias="default", host="milvus-standalone", port="19530")
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
        embeddings.append(values.tolist())

    return {"UUIDS": uuids, "Regions": regions, "Embeddings": embeddings}


def insert_embeddings(milvus_data: Dict[str, List[Any]], collection_name: str) -> None:
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


def search_embeddings_dict(
    embeddings_dict: Dict[str, Dict[str, Any]],
    collection_name: str,
    search_params: Dict[str, Any],
    top_k: int,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search approximate nearest neighbor embeddings in the Milvus vector database.

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
        query_vector = values.tolist()

        try:
            results = collection.search(
                data=[query_vector],  # Type List required
                anns_field="vector",
                param=search_params,
                limit=top_k,
                partition_names=[region],
                output_fields=[PipelineDictKeys.UUID.value],
            )

            results_by_region[region] = []
            for hits in results:
                for hit in hits:
                    results_by_region[region].append(
                        {
                            "id": hit.id,
                            PipelineDictKeys.UUID.value: hit.entity.get(PipelineDictKeys.UUID.value),
                            # that's cosine SIMILARITY, even though they call it distance
                            PipelineDictKeys.SIMILARITY.value: hit.distance,
                        }
                    )
        except Exception as e:
            print(f"Search query failed for region '{region}': {e}")
            results_by_region[region] = []

    collection.release()
    print(f"Collection '{collection_name}' released from memory.")

    return results_by_region


def delete_embeddings(uuid_to_delete: str, collection_name: str) -> None:
    """
    Deletes all embeddings associated with a given UUID from the specified Milvus collection.

    Args:
        uuid_to_delete (str): The UUID of the embeddings to be deleted.
        collection_name (str): The name of the Milvus collection.

    Returns:
        None
    """
    connect_to_host()

    if not utility.has_collection(collection_name):
        print(f"Collection with name '{collection_name}' not found.")
        return

    collection = Collection(name=collection_name)
    collection.delete(f"uuid == '{uuid_to_delete}'")
    print(f"Entries with UUID '{uuid_to_delete}' deleted successfully.")


def query_uuid(uuid_to_query: str, collection_name: str) -> List[Dict[str, Any]]:
    """
    Queries all embeddings associated with a given UUID from the specified Milvus collection.

    Args:
        uuid_to_query (str): The UUID of the embeddings to be retrieved.
        collection_name (str): The name of the Milvus collection.

    Returns:
        List[Dict[str, Any]]: A list of matching records, where each record is a dictionary containing
        fields such as 'uuid', 'region', and 'vector'. Returns an empty list if no matches are found.
    """
    connect_to_host()

    if not utility.has_collection(collection_name):
        print(f"Collection with name '{collection_name}' not found.")
        return []

    collection = Collection(name=collection_name)
    collection.load()

    try:
        results = collection.query(expr=f"uuid == '{uuid_to_query}'", output_fields=["id", "uuid", "region"])
    except Exception as e:
        print(f"Error during query execution: {e}")
        return []

    if not results:  # Bessere Überprüfung für leere Listen
        print(f"No matching entries found for UUID: {uuid_to_query}")
        return []

    return results


def drop_collection(collection_name: str) -> None:
    """
    Drops (deletes) a Milvus collection if it exists.

    Args:
        collection_name (str): The name of the Milvus collection to be deleted.

    Returns:
        None
    """
    connect_to_host()  # Ensure connection to Milvus before attempting deletion

    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
        print(f"Collection '{collection_name}' deleted successfully!")
    else:
        print(f"Collection '{collection_name}' does not exist.")
