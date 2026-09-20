from typing import Any


TYPE_MAP = {
    "string": "String",
    "number": "Float",
    "integer": "Int",
    "boolean": "Boolean",
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

    for model in models:
        model_name = model.get("name")

        if not model_name:
            continue

        lines.append(f"model {model_name} {{")

        for field in model.get("fields", []):
            name = field.get("name")

            if not name:
                continue

            field_type = map_field_type(
                field.get("type", "string")
            )

            modifiers = []

            if field.get("generated"):
                modifiers.extend([
                    "@id",
                    "@default(cuid())",
                ])

            if field.get("unique"):
                modifiers.append("@unique")

            modifier_text = ""

            if modifiers:
                modifier_text = " " + " ".join(modifiers)

            lines.append(
                f"  {name} {field_type}{modifier_text}"
            )

        lines.append("}")
        lines.append("")

    return "\n".join(lines)