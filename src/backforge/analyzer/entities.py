def infer_entities_from_request_bodies(
    request_bodies: list[dict],
) -> list[dict]:
    """
    Infer candidate domain entities from
    request body fields.
    """

    entities = []

    for request in request_bodies:

        endpoint = request.get(
            "endpoint",
            "",
        )

        fields = request.get(
            "fields",
            [],
        )

        if not fields:
            continue

        if endpoint.endswith("/bookings"):
            entity_name = "Booking"

        else:
            continue

        entities.append(
            {
                "name": entity_name,
                "confidence": "medium",
                "source": {
                    "endpoint": endpoint,
                },
                "fields": fields,
            }
        )

    return entities