from typing import Any


TYPE_MAP = {
    "string": "String",
    "number": "Float",
    "integer": "Int",
    "boolean": "Boolean",
    "date": "DateTime",
}


def map_field_type(field_type: str) -> str:
    return TYPE_MAP.get(
        field_type.lower(),
        "String",
    )


def generate_prisma_schema(
    database: dict[str, Any],
) -> str:
    models = database.get("models", [])

    lines = [
        "generator client {",
        '  provider = "prisma-client-js"',
        "}",
        "",
        "datasource db {",
        '  provider = "postgresql"',
        "}",
        "",
    ]

    model_names = {
        model.get("name")
        for model in models
    }

    for model in models:
        model_name = model.get("name")

        if not model_name:
            continue

        lines.append(
            f"model {model_name} {{"
        )

        for field in model.get("fields", []):
            name = field.get("name")

            if not name:
                continue

            # ------------------------------------------
            # Session -> User relationship
            # ------------------------------------------

            if (
                model_name == "Session"
                and name == "userId"
                and "User" in model_names
            ):
                lines.append(
                    "  userId String"
                )
                lines.append(
                    "  user User @relation("
                    'fields: [userId], '
                    "references: [id], "
                    "onDelete: Cascade)"
                )
                continue

            field_type = map_field_type(
                field.get("type", "string")
            )

            modifiers = []

            if field.get("generated"):
                modifiers.extend(
                    [
                        "@id",
                        "@default(cuid())",
                    ]
                )

            if field.get("unique"):
                modifiers.append("@unique")

            modifier_text = (
                " " + " ".join(modifiers)
                if modifiers
                else ""
            )

            lines.append(
                f"  {name} "
                f"{field_type}"
                f"{modifier_text}"
            )

        # ------------------------------------------
        # User -> Sessions relationship
        # ------------------------------------------

        if (
            model_name == "User"
            and "Session" in model_names
        ):
            lines.append(
                "  sessions Session[]"
            )

        lines.append("}")
        lines.append("")

    return "\n".join(lines)