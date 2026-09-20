def generate_database_models(
    entities: list[dict],
) -> list[dict]:
    models = []

    for entity in entities:
        name = entity.get("name")
        fields = entity.get("fields", [])

        if not name:
            continue

        model_fields = [
            {
                "name": "id",
                "type": "string",
                "generated": True,
            }
        ]

        for field in fields:
            model_field = {
                "name": field.get("name"),
                "type": field.get("type", "unknown"),
                "generated": False,
            }

            if field.get("unique"):
                model_field["unique"] = True

            model_fields.append(model_field)

        models.append(
            {
                "name": name,
                "source_confidence": entity.get(
                    "confidence",
                    "unknown",
                ),
                "fields": model_fields,
            }
        )

    return models