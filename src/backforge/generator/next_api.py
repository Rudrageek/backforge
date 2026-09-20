
from backforge.generator.utils import prisma_delegate_name
from typing import Any


def generate_next_api_route(
    api_spec: dict[str, Any],
    model_name: str,
) -> str:
    """
    Generate a Next.js POST API route that
    validates input and persists the record
    through Prisma.
    """

    method = api_spec.get("method", "").upper()
    request_body = api_spec.get("request_body", [])

    if method != "POST":
        raise ValueError(
            f"Unsupported method: {method}"
        )

    fields = [
        field.get("name")
        for field in request_body
        if field.get("name")
    ]

    validation_lines = []

    for field in fields:
        validation_lines.append(
            f"  if (!body.{field}) {{"
        )
        validation_lines.append(
            f'    return Response.json('
            f'{{ error: "{field} is required" }}, '
            f'{{ status: 400 }}'
            f');'
        )
        validation_lines.append("  }")

    validation = "\n".join(validation_lines)

    create_fields = ",\n".join(
        f"      {field}: body.{field}"
        for field in fields
    )

    return f"""import {{ NextRequest }} from "next/server";
import {{ prisma }} from "@/lib/prisma";

export async function POST(
  request: NextRequest
) {{
  const body = await request.json();

{validation}

  const record = await prisma.{prisma_delegate_name(model_name)}.create({{
    data: {{
{create_fields}
    }},
  }});

  return Response.json(
    record,
    {{ status: 201 }}
  );
}}
"""