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


def detect_api_calls_from_source(
    source_code: str,
) -> list[dict]:
    """
    Detect fetch() API calls from TypeScript/TSX source.
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

            if (
                function_node
                and function_node.type
                == "identifier"
                and function_node.text.decode(
                    "utf-8"
                )
                == "fetch"
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

                        url_node = (
                            named_children[0]
                        )

                        url = extract_string(
                            url_node
                        )

                        if url:
                            method = (
                                extract_method(
                                    arguments
                                )
                            )

                            results.append(
                                {
                                    "method": method,
                                    "endpoint": url,
                                }
                            )

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return results


def extract_string(node) -> str | None:
    """
    Extract a string literal from a Tree-sitter node.
    """

    if node.type in {
        "string",
        "string_fragment",
    }:
        text = node.text.decode(
            "utf-8"
        )

        return text.strip(
            "\"'`"
        )

    return None


def extract_method(arguments_node) -> str:
    """
    Extract HTTP method from fetch options.

    Defaults to GET.
    """

    for child in arguments_node.named_children:

        if child.type != "object":
            continue

        for property_node in (
            child.named_children
        ):

            if property_node.type != "pair":
                continue

            key_node = (
                property_node.child_by_field_name(
                    "key"
                )
            )

            value_node = (
                property_node.child_by_field_name(
                    "value"
                )
            )

            if not key_node or not value_node:
                continue

            key = key_node.text.decode(
                "utf-8"
            )

            if key != "method":
                continue

            value = extract_string(
                value_node
            )

            if value:
                return value.upper()

    return "GET"


def analyze_api_calls_in_project(
    project_path: str,
) -> list[dict]:
    """
    Scan TSX and TS files for fetch() calls.
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

            calls = (
                detect_api_calls_from_source(
                    source_code
                )
            )

            for call in calls:
                results.append(
                    {
                        **call,
                        "file": str(path),
                    }
                )

    return results