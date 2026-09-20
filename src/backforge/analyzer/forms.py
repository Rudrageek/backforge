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


def read_source_file(path: Path) -> str:
    """
    Read a source file as UTF-8 text.
    """

    return path.read_text(
        encoding="utf-8"
    )


def detect_forms_from_source(
    source_code: str,
) -> list[dict]:
    """
    Detect JSX forms and their input fields
    from a TSX source file.
    """

    parser = create_typescript_parser()

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    forms = []

    def walk(node):
        if node.type == "jsx_element":
            opening = node.child_by_field_name(
                "open_tag"
            )

            if opening:
                tag_name = opening.child_by_field_name(
                    "name"
                )

                if (
                    tag_name
                    and tag_name.text.decode("utf-8")
                    == "form"
                ):
                    forms.append(
                        analyze_form(node)
                    )

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return forms


def analyze_form(form_node) -> dict:
    """
    Analyze one JSX form.
    """

    fields = []

    def walk(node):
        if node.type == "jsx_self_closing_element":
            opening = node.child_by_field_name(
                "name"
            )

            if opening:
                tag_name = opening.text.decode(
                    "utf-8"
                )

                if tag_name in {
                    "input",
                    "textarea",
                    "select",
                }:
                    fields.append(
                        analyze_field(node)
                    )

        elif node.type == "jsx_opening_element":
            tag_name_node = node.child_by_field_name(
                "name"
            )

            if tag_name_node:
                tag_name = (
                    tag_name_node.text.decode(
                        "utf-8"
                    )
                )

                if tag_name in {
                    "input",
                    "textarea",
                    "select",
                }:
                    fields.append(
                        analyze_field(node)
                    )

        for child in node.children:
            walk(child)

    walk(form_node)

    return {
        "fields": fields,
    }


def analyze_field(node) -> dict:
    """
    Extract useful information from a JSX field.
    """

    field = {
        "element": None,
        "name": None,
        "type": None,
    }

    name_node = node.child_by_field_name(
        "name"
    )

    if name_node:
        field["element"] = (
            name_node.text.decode("utf-8")
        )

    for attribute in node.children:

        if attribute.type != "jsx_attribute":
            continue

        attribute_parts = [
            child
            for child in attribute.children
        ]

        if not attribute_parts:
            continue

        attribute_name = attribute_parts[0]

        attribute_name_text = (
            attribute_name.text.decode(
                "utf-8"
            )
        )

        attribute_value = None

        if len(attribute_parts) > 1:
            value_node = attribute_parts[-1]

            attribute_value = (
                value_node.text.decode(
                    "utf-8"
                ).strip("\"'")
            )

        if attribute_name_text == "name":
            field["name"] = attribute_value

        elif attribute_name_text == "type":
            field["type"] = attribute_value

    return field


def analyze_forms_in_project(
    project_path: str,
) -> list[dict]:
    """
    Scan all TSX files in a project and detect forms.
    """

    root = Path(project_path)

    results = []

    for path in root.rglob("*.tsx"):

        if "node_modules" in path.parts:
            continue

        source_code = read_source_file(path)

        forms = detect_forms_from_source(
            source_code
        )

        for form in forms:
            form["file"] = str(path)
            results.append(form)

    return results