from typing import Any


def generate_api_spec(
    api: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Generate backend API specifications
    from frontend API requirements.
    """

    specifications = []

    request_bodies = {
        request["endpoint"]: request
        for request in api.get("request_bodies", [])
    }

    for route in api.get("missing", []):
        method = route.get("method")
        endpoint = route.get("endpoint")

        if not method or not endpoint:
            continue

        request = request_bodies.get(
            endpoint,
            {},
        )

        specifications.append(
            {
                "method": method,
                "endpoint": endpoint,
                "request_body": request.get(
                    "fields",
                    [],
                ),
                "response": {
                    "type": "object",
                },
                "validation": True,
                "database_operation": (
                    "create"
                    if method.upper() == "POST"
                    else "unknown"
                ),
            }
        )

    return specifications