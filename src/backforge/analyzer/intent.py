def infer_form_intent(
    form: dict,
    route: str | None = None,
) -> dict:
    """
    Infer the likely purpose of a form from
    observable frontend evidence.
    """

    fields = form.get("fields", [])

    field_names = {
        field.get("name", "").lower()
        for field in fields
        if field.get("name")
    }

    field_types = {
        field.get("type", "").lower()
        for field in fields
        if field.get("type")
    }

    route_text = (
        route.lower()
        if route
        else ""
    )

    if (
        "email" in field_names
        and "password" in field_names
        and "login" in route_text
    ):
        return {
            "intent": "login",
            "confidence": "high",
            "evidence": [
                "route contains 'login'",
                "email field detected",
                "password field detected",
            ],
        }

    if (
        "email" in field_names
        and "password" in field_names
    ):
        return {
            "intent": "authentication",
            "confidence": "medium",
            "evidence": [
                "email field detected",
                "password field detected",
            ],
        }

    if "password" in field_types:
        return {
            "intent": "authentication",
            "confidence": "low",
            "evidence": [
                "password input detected",
            ],
        }

    return {
        "intent": "unknown",
        "confidence": "low",
        "evidence": [],
    }