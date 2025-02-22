# Milvus Script

A script that provides various operations related to embeddings in the [Milvus](https://milvus.io/) vector database. It creates and manages collections, inserts/searches embeddings, and deletes/query records by UUID.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
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

## Usage

- Make sure that Milvus Standalone is running (e.g., via Docker or a local setup).


