import json
from pathlib import Path


def read_package_json(project_path: str) -> dict:
    """
    Read package.json from a frontend project.
    """

    package_path = Path(project_path) / "package.json"

    if not package_path.exists():
        return {}

    try:
        with package_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def get_dependencies(package_data: dict) -> dict:
    """
    Return combined dependencies and devDependencies.
    """

    dependencies = package_data.get(
        "dependencies",
        {},
    )

    dev_dependencies = package_data.get(
        "devDependencies",
        {},
    )

    return {
        **dependencies,
        **dev_dependencies,
    }


def detect_framework(package_data: dict) -> str:
    """
    Detect the frontend framework from package.json.
    """

    dependencies = get_dependencies(package_data)

    if "next" in dependencies:
        return "Next.js"

    if "vite" in dependencies and (
        "react" in dependencies
    ):
        return "React + Vite"

    if "react" in dependencies:
        return "React"

    if "vue" in dependencies:
        return "Vue"

    if "@angular/core" in dependencies:
        return "Angular"

    if "svelte" in dependencies:
        return "Svelte"

    return "Unknown"