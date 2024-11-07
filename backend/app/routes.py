from fastapi import APIRouter, WebSocket

from .api.rest import get_index
from .api.websocket import websocket_endpoint
from .api.graphql import graphql_app


router = APIRouter()

# REST API routes
@router.get("/")
async def get():
    return await get_index()

# Websocket routes
@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)

# GraphQL routes
router.include_router(graphql_app, prefix="/graphql")
