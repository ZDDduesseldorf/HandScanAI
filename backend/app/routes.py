from fastapi import APIRouter

from .api.rest import rest_router
from .api.websocket import ws_router
from .api.graphql import graphql_router

router = APIRouter()

# REST API router
router.include_router(rest_router, prefix="/rest")

# Websocket router
router.include_router(ws_router, prefix="/ws")

# GraphQL router
router.include_router(graphql_router, prefix="/graphql")
