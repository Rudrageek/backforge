from pathlib import Path
import re


BACKEND_EXTENSIONS = {
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
    ".venv",
}


def detect_backend_routes_from_source(
    source_code: str,
) -> list[dict]:
    """
    Detect common Express-style backend routes
    from JavaScript or TypeScript source code.
    """

    routes = []

    pattern = re.compile(
        r"""
        \b
        (get|post|put|patch|delete)
        \s*
        \(
        \s*
        ["'`]([^"'`]+)["'`]
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    for match in pattern.finditer(
        source_code
    ):
        method = match.group(1).upper()
        endpoint = match.group(2)

        routes.append(
            {
                "method": method,
                "endpoint": endpoint,
            }
        )

    return routes


def analyze_backend_routes(
    project_path: str,
) -> list[dict]:
    """
    Scan backend source files and detect
    Express-style HTTP routes.
    """

    root = Path(project_path)

    results = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        if path.suffix.lower() not in (
            BACKEND_EXTENSIONS
        ):
            continue

        source_code = path.read_text(
            encoding="utf-8"
        )

        routes = (
            detect_backend_routes_from_source(
                source_code
            )
        )

        for route in routes:
            results.append(
                {
                    **route,
                    "file": str(path),
                }
            )

    return results