from pathlib import Path


def write_generated_file(
    output_root: str,
    relative_path: str,
    content: str,
) -> Path:
    """
    Write generated backend code to the output project.
    """

    root = Path(output_root)
    file_path = root / relative_path

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return file_path