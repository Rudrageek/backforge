from pathlib import Path


def detect_nextjs_routes(project_path: str) -> list[str]:
    """
    Detect routes from a Next.js App Router project.
    """

    root = Path(project_path)

    app_directories = [
        root / "app",
        root / "src" / "app",
    ]

    app_directory = None

    for directory in app_directories:
        if directory.exists() and directory.is_dir():
            app_directory = directory
            break

    if app_directory is None:
        return []

    routes = []

    for page_file in app_directory.rglob("page.*"):
        if page_file.suffix not in {
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
        }:
            continue

        relative = page_file.parent.relative_to(
            app_directory
        )

        if str(relative) == ".":
            route = "/"
        else:
            parts = relative.parts

            route = "/" + "/".join(parts)

        routes.append(route)

    return sorted(set(routes))