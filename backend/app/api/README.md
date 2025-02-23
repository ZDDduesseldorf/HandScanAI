# API Documentation

This document provides an overview of the API endpoints and functionalities implemented in the `graphql.py`, `rest.py`, and `websocket.py` files.

## Table of Contents

- [API Documentation](#api-documentation)
  - [Table of Contents](#table-of-contents)
  - [GraphQL API](#graphql-api)
    - [Schema](#schema)
    - [Queries](#queries)
    - [Mutations](#mutations)
  - [REST API](#rest-api)
    - [Endpoints](#endpoints)
  - [WebSocket API](#websocket-api)

## GraphQL API

The GraphQL API is implemented using Strawberry and provides CRUD operations to interact with the backend.

### Schema

The schema defines the different request and response data objects.

### Queries

Queries define the different functions for querying data.

### Mutations

Mutations are used to manipulate data in the database.

## REST API

The REST API primarily defines endpoints to load images in the frontend.

### Endpoints

- `GET /`: Returns a welcome message.
- `GET /image`: Retrieves an image by its UUID.
- `GET /image_nearest_neigbhours`: Retrieves the nearest neighbor image by its UUID.

## WebSocket API

The WebSocket API is implemented using FastAPI and provides a WebSocket endpoint for the webcam flow. Check out the function's docstring for instructions on how to use it.
