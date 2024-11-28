from typing import List, Optional
from fastapi import APIRouter
import strawberry
from datetime import datetime
from strawberry.fastapi import GraphQLRouter

from app.db.models import TestModel


@strawberry.type
class TestModelType:
    id: strawberry.ID
    name: str
    description: Optional[str]
    created_at: datetime


@strawberry.input
class TestModelInput:
    name: str
    description: Optional[str]


@strawberry.type
class Query:
    @strawberry.field
    async def get_test_models(self) -> List[TestModelType]:
        test_models = await TestModel.find_all().to_list()
        return [TestModelType(**model.model_dump()) for model in test_models]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_test_model(self, input: TestModelInput) -> TestModelType:
        test_model = TestModel(name=input.name, description=input.description)
        await test_model.insert()
        return TestModelType(**test_model.model_dump())

    @strawberry.mutation
    async def update_test_model(self, id: strawberry.ID, input: TestModelInput) -> Optional[TestModelType]:
        test_model = await TestModel.get(id)
        if test_model:
            test_model.name = input.name
            test_model.description = input.description
            await test_model.save()
            return TestModelType(**test_model.model_dump())
        return None

    @strawberry.mutation
    async def delete_test_model(self, id: strawberry.ID) -> bool:
        test_model = await TestModel.get(id)
        if test_model:
            await test_model.delete()
            return True
        return False


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)

router = APIRouter()
router.include_router(graphql_router, prefix="/graphql")
