from pathlib import Path


BACKEND_INDICATORS = {
    "server.js",
    "server.ts",
    "app.js",
    "app.ts",
    "main.py",
    "manage.py",
    "Dockerfile",
}


BACKEND_DIRECTORIES = {
    "backend",
    "server",
    "api",
}


def detect_backend(
    project_path: str,
) -> dict:
    """
    Detect basic indicators of an existing backend.
    """

    root = Path(project_path)

    indicator_files = []
    indicator_directories = []

    for path in root.rglob("*"):

        if any(
            ignored in path.parts
            for ignored in {
                "node_modules",
                ".git",
                ".next",
                "dist",
                "build",
                ".venv",
            }
        ):
            continue

        if path.is_file():
            if path.name in BACKEND_INDICATORS:
                indicator_files.append(
                    str(path)
                )

        elif path.is_dir():
            if path.name.lower() in (
                BACKEND_DIRECTORIES
            ):
                indicator_directories.append(
                    str(path)
                )

    detected = bool(
        indicator_files
        or indicator_directories
    )

    return {
        "detected": detected,
        "indicator_files": indicator_files,
        "indicator_directories": indicator_directories,
    }