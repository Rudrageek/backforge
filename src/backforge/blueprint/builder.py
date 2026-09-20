from backforge.analyzer.auth import generate_user_entity
from backforge.analyzer.database import infer_database_requirement
from backforge.analyzer.entities import infer_entities_from_request_bodies
from backforge.analyzer.request_body import analyze_request_bodies_in_project
from backforge.analyzer.schema import generate_database_models
from backforge.blueprint.specification import BackendSpecification


def build_specification(blueprint) -> BackendSpecification:
    """
    Build the backend specification from the
    application blueprint.
    """

    specification = BackendSpecification()

    request_bodies = (
        analyze_request_bodies_in_project(
            blueprint.project_path
        )
    )

    entities = infer_entities_from_request_bodies(
        request_bodies
    )

    authentication = blueprint.requirements.get(
        "authentication",
        {}
    )

    # --------------------------------------------------
    # Authentication
    # --------------------------------------------------

    if authentication.get("detected"):
        specification.authentication = {
            "enabled": True,
            "method": None,
            "status": "configuration_required",
        }

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    database = infer_database_requirement(
        entities
    )

    specification.entities = entities

    specification.api = {
        "required": blueprint.api_calls,
        "missing": blueprint.missing_api_calls,
        "request_bodies": request_bodies,
    }

    specification.database = database

    return specification