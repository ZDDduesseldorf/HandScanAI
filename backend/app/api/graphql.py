from fastapi import APIRouter
import strawberry

from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

router = APIRouter()
router.add_route("/", graphql_app)