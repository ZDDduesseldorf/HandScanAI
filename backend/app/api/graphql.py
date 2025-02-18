from datetime import datetime, timezone
from typing import Optional, List

import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from app.db.models import ScanEntry
from pipelines.inference_pipeline import run_inference_pipeline


@strawberry.type
class ScanEntryType:
    id: strawberry.ID
    image_exists: bool
    real_age: Optional[int]
    real_gender: Optional[int]
    confirmed: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @strawberry.field
    async def image_exists(self) -> bool:
        scan_entry = await ScanEntry.get(self.id)
        return scan_entry.image_exists


@strawberry.input
class ScanEntryInput:
    real_age: Optional[int] = None
    real_gender: Optional[int] = None
    confirmed: Optional[bool] = False


@strawberry.type
class ScanResultType:
    id: strawberry.ID
    min_age: float
    max_age: float
    classified_age: float
    confidence_age: float
    classified_gender: float
    confidence_gender: float


@strawberry.type
class ScanResultNearestNeighboursType:
    id: strawberry.ID
    age: float
    gender: float
    region: str


@strawberry.type
class ScanResultsWrapper:
    result_classifier: ScanResultType
    nearest_neigbhour_info: List[ScanResultNearestNeighboursType]


@strawberry.type
class Query:
    @strawberry.field
    async def get_scan_entry_models(self) -> list[ScanEntryType]:
        scan_entry_models = await ScanEntry.find_all().to_list()
        return [ScanEntryType(**model.model_dump()) for model in scan_entry_models]

    @strawberry.field
    async def get_scan_entry_model(self, id: strawberry.ID) -> ScanEntryType:
        scan_entry_model = await ScanEntry.get(id)
        if scan_entry_model is None:
            raise ValueError("ScanEntry not found")
        return ScanEntryType(**scan_entry_model.model_dump())

    @strawberry.field
    async def get_scan_result(self, id: strawberry.ID) -> ScanResultsWrapper:
        scan_entry_model = await ScanEntry.get(id)

        if scan_entry_model is None:
            raise ValueError("ScanEntry not found")

        if not scan_entry_model.image_exists:
            raise ValueError("ScanEntry doesn't have a query image")

        result, result_knn_info = run_inference_pipeline(id, testing=False, use_milvus=False)

        if result.empty or result_knn_info.empty:
            raise ValueError("No result from inference pipeline")

        result_dict = result.to_dict(orient="records")[0]
        result_knn_info_dict = result_knn_info.to_dict(orient="records")

        return ScanResultsWrapper(
            result_classifier=ScanResultType(
                id=id,
                confidence_age=result_dict["confidence_age"],
                classified_age=result_dict["classified_age"],
                min_age=result_dict["min_age"],
                max_age=result_dict["max_age"],
                classified_gender=result_dict["classified_gender"],
                confidence_gender=result_dict["confidence_gender"],
            ),
            nearest_neigbhour_info=[
                ScanResultNearestNeighboursType(
                    id=row["uuid"],
                    age=row["age"],
                    gender=row["gender"],
                    region=row["region"],
                )
                for row in result_knn_info_dict
            ],
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_scan_entry_model(self) -> ScanEntryType:
        scan_entry_model = ScanEntry()
        await scan_entry_model.insert()
        return ScanEntryType(**scan_entry_model.model_dump())

    @strawberry.mutation
    async def update_scan_entry_model(self, id: strawberry.ID, input: ScanEntryInput) -> ScanEntryType:
        scan_entry_model = await ScanEntry.get(id)
        if scan_entry_model is None:
            raise ValueError("ScanEntry not found")

        if input.real_age is not None:
            scan_entry_model.real_age = input.real_age

        if input.real_gender is not None:
            scan_entry_model.real_gender = input.real_gender

        if input.confirmed is not None:
            scan_entry_model.confirmed = input.confirmed

        scan_entry_model.updated_at = datetime.now(timezone.utc)

        await scan_entry_model.save()
        return ScanEntryType(**scan_entry_model.model_dump())

    @strawberry.mutation
    async def delete_scan_entry_model(self, id: strawberry.ID) -> bool:
        scan_entry_model = await ScanEntry.get(id)
        if scan_entry_model is None:
            raise ValueError("ScanEntry not found")

        await scan_entry_model.delete()
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema=schema)

router = APIRouter()
router.include_router(graphql_router, prefix="/graphql")
