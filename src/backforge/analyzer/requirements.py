def analyze_requirements(
    blueprint,
) -> dict:
    """
    Analyze an ApplicationBlueprint and produce
    backend requirements without making assumptions
    about external providers.
    """

    requirements = {
        "api": {
            "implemented": blueprint.implemented_api_calls,
            "missing": blueprint.missing_api_calls,
            "extra": blueprint.extra_backend_routes,
        },
        "authentication": {
            "detected": False,
            "status": "not_detected",
            "reason": None,
        },
        "database": {
            "status": "undetermined",
        },
        "payments": {
            "status": "not_detected",
        },
        "email": {
            "status": "not_detected",
        },
        "storage": {
            "status": "not_detected",
        },
    }

    login_forms = [
        form
        for form in blueprint.forms
        if form.get("intent")
        in {
            "login",
            "authentication",
        }
    ]

    if login_forms:
        requirements[
            "authentication"
        ] = {
            "detected": True,
            "status": "configuration_required",
            "reason": (
                "Authentication-related form "
                "detected in the frontend."
            ),
        }

    return requirements