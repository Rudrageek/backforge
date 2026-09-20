from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_typescript


def create_typescript_parser() -> Parser:
    """
    Create a Tree-sitter parser for TSX.
    """

    language = Language(
        tree_sitter_typescript.language_tsx()
    )

    return Parser(language)


def extract_object_fields(
    node,
) -> list[dict]:
    """
    Extract fields from a JavaScript/TypeScript
    object literal.
    """

    fields = []

    if node.type != "object":
        return fields

    for property_node in node.named_children:

        if property_node.type != "pair":
            continue

        key_node = property_node.child_by_field_name(
            "key"
        )

        value_node = property_node.child_by_field_name(
            "value"
        )

        if not key_node:
            continue

        field_name = key_node.text.decode(
            "utf-8"
        )

        field_type = infer_value_type(
            value_node
        )

        fields.append(
            {
                "name": field_name,
                "type": field_type,
            }
        )

    return fields


def infer_value_type(
    node,
) -> str:
    """
    Infer a simple type from a JavaScript/TypeScript
    value node.
    """

    if node is None:
        return "unknown"

    node_type = node.type

    if node_type in {
        "string",
        "template_string",
    }:
        return "string"

    if node_type in {
        "number",
        "number_literal",
    }:
        return "number"

    if node_type in {
        "true",
        "false",
    }:
        return "boolean"

    if node_type in {
        "array",
        "array_pattern",
    }:
        return "array"

    if node_type == "object":
        return "object"

    return "unknown"


def detect_request_bodies_from_source(
    source_code: str,
) -> list[dict]:
    """
    Detect JSON request bodies passed to fetch().
    """

    parser = create_typescript_parser()

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    results = []

    def walk(node):

        if node.type == "call_expression":

            function_node = (
                node.child_by_field_name(
                    "function"
                )
            )

            if not function_node:
                for child in node.children:
                    walk(child)
                return

            if (
                function_node.type == "identifier"
                and function_node.text.decode(
                    "utf-8"
                ) == "fetch"
            ):
                arguments = (
                    node.child_by_field_name(
                        "arguments"
                    )
                )

                if arguments:
                    named_children = (
                        arguments.named_children
                    )

                    if named_children:

                        endpoint_node = (
                            named_children[0]
                        )

                        endpoint = (
                            extract_string(
                                endpoint_node
                            )
                        )

                        if endpoint:

                            body = (
                                find_json_body(
                                    arguments
                                )
                            )

                            if body:
                                results.append(
                                    {
                                        "endpoint": endpoint,
                                        "fields": body,
                                    }
                                )

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return results


def find_json_body(
    arguments_node,
) -> list[dict]:
    """
    Find JSON.stringify({ ... }) inside fetch options.
    """

    for child in arguments_node.named_children:

        if child.type != "object":
            continue

        for property_node in child.named_children:

            if property_node.type != "pair":
                continue

            key_node = property_node.child_by_field_name(
                "key"
            )

            value_node = property_node.child_by_field_name(
                "value"
            )

            if not key_node or not value_node:
                continue

            key = key_node.text.decode(
                "utf-8"
            )

            if key != "body":
                continue

            if value_node.type != "call_expression":
                continue

            function_node = (
                value_node.child_by_field_name(
                    "function"
                )
            )

            if not function_node:
                continue

            if (
                function_node.type == "member_expression"
                and function_node.text.decode(
                    "utf-8"
                ).startswith("JSON.stringify")
            ):
                arguments = (
                    value_node.child_by_field_name(
                        "arguments"
                    )
                )

                if not arguments:
                    continue

                if not arguments.named_children:
                    continue

                object_node = (
                    arguments.named_children[0]
                )

                return extract_object_fields(
                    object_node
                )

    return []


def extract_string(
    node,
) -> str | None:
    """
    Extract a string literal.
    """

    if node.type in {
        "string",
        "string_fragment",
    }:
        return node.text.decode(
            "utf-8"
        ).strip("\"'`")

    return None


def analyze_request_bodies_in_project(
    project_path: str,
) -> list[dict]:
    """
    Scan TS and TSX files for fetch request bodies.
    """

    root = Path(project_path)

    results = []

    for extension in (
        "*.tsx",
        "*.ts",
    ):

        for path in root.rglob(
            extension
        ):

            if any(
                ignored in path.parts
                for ignored in {
                    "node_modules",
                    ".git",
                    ".next",
                    "dist",
                    "build",
                }
            ):
                continue

            source_code = path.read_text(
                encoding="utf-8"
            )

            bodies = (
                detect_request_bodies_from_source(
                    source_code
                )
            )

            for body in bodies:
                results.append(
                    {
                        **body,
                        "file": str(path),
                    }
                )

    return results