from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}


IGNORED_DIRECTORIES = {
    "node_modules",
    ".git",
    ".next",
    "dist",
    "build",
    "coverage",
}


def find_source_files(project_path: str) -> list[Path]:
    """
    Find JavaScript and TypeScript source files
    inside a frontend project.
    """

    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {root}"
        )

    source_files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        source_files.append(path)

    return sorted(source_files)