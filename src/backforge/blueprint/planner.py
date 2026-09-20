from backforge.blueprint.plan import BackendPlan
from backforge.generator.api import generate_api_spec
from backforge.generator.prisma import generate_prisma_schema


def build_backend_plan(specification) -> BackendPlan:
    """
    Convert the backend specification into
    an implementation-oriented backend plan.
    """

    api_spec = generate_api_spec(
        specification.api
    )

    prisma_schema = generate_prisma_schema(
        specification.database
    )

    database = {
        **specification.database,
        "schema": prisma_schema,
    }

    integrations = []

    if specification.authentication.get("enabled"):
        integrations.append(
            {
                "type": "authentication",
                "method": specification.authentication.get(
                    "method"
                ),
                "status": specification.authentication.get(
                    "status"
                ),
            }
        )

    return BackendPlan(
        database=database,
        api=api_spec,
        authentication=specification.authentication,
        integrations=integrations,
    )