def infer_database_requirement(
    entities: list[dict],
) -> dict:
    """
    Infer whether persistent storage may be required
    from candidate domain entities.
    """

    if not entities:
        return {
            "detected": False,
            "status": "not_detected",
            "entities": [],
        }

    return {
        "detected": True,
        "status": "configuration_required",
        "reason": (
            "Candidate persistent entities "
            "were detected in the frontend."
        ),
        "entities": [
            entity["name"]
            for entity in entities
        ],
    }