from backforge.analyzer.auth import generate_user_entity
from backforge.analyzer.schema import generate_database_models
from backforge.blueprint.specification import BackendSpecification


def apply_answer(
    specification: BackendSpecification,
    question_id: str,
    answer: str,
) -> BackendSpecification:
    """
    Apply a configuration answer to the
    backend specification.
    """

    if question_id == "authentication_method":

        specification.authentication = {
            "enabled": True,
            "method": answer,
            "status": "configured",
        }

        if answer == "email_password":

            user_entity = generate_user_entity()

            existing_entities = [
                entity
                for entity in specification.entities
                if entity.get("name") != "User"
            ]

            specification.entities = (
                existing_entities
                + [user_entity]
            )

            specification.database = {
                **specification.database,
                "detected": True,
                "status": "configuration_required",
                "entities": [
                    entity["name"]
                    for entity in specification.entities
                ],
                "models": generate_database_models(
                    specification.entities
                ),
            }

    elif question_id == "database_provider":

        specification.database = {
            **specification.database,
            "provider": answer,
            "status": "configured",
        }

    return specification