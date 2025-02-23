# Milvus Script

A script that provides various operations related to embeddings in the [Milvus](https://milvus.io/) vector database. It creates and manages collections, inserts/searches embeddings, and deletes/query records by UUID.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Container](#usage)
- [Usage](#usage)

---

## Overview

This script focuses on handling embeddings (e.g., hand-region embeddings) within Milvus. It includes:

- Creating a collection with partitions (`create_miluvs_collection()`)
- Inserting embeddings (`add_embeddings_to_milvus()`)
- Searching with configurable parameters (`search_embeddings_dict()`)
- Querying  by UUID (`query_uuid`)
- Deleting by UUID (`delete_embeddings`)

In the broader pipeline:
- **`add_embeddings_to_milvus()`** is mainly used in the **`initial_data_pipeline`** and **`add_new_embeddings_pipeline`**.  
- **`search_embeddings_dict()`** is primarily used in the **`inference_pipeline`**.

---

## Requirements

- **Python**: Version 3.10
- **Milvus**: e.g., version 2.5
- **Dependencies**:
  - `pymilvus` (Milvus Python client)
  - `torch` (used for handling embeddings)
- A running Milvus instance (defaults in the script: `host="milvus-standalone"`, `port="19530"`)

---

## Container Architecture

In this project, we use Milvus as a vector database. Milvus provides several containers, each serving a specific purpose:

- **Milvus Standalone Container:**  
  This container bundles all the necessary components into a single unit. It is ideally suited for development and testing environments where a quick and simple setup is paramount.

- **Milvus ETCD Container:**  
  ETCD is a distributed key-value database used for managing configurations and metadata within the cluster. Running ETCD in a separate container ensures reliable and scalable system coordination.

- **Milvus MinIO Container:**  
  MinIO offers S3-compatible object storage responsible for the persistent storage of large datasets. A dedicated MinIO container allows independent management and backup of data, which is particularly advantageous in production environments.

This modular architecture enables independent scaling, maintenance, and optimization of each component, thereby enhancing the flexibility and stability of our system.

---
## Usage

- Make sure that Milvus Standalone is running (e.g., via Docker or a local setup).

