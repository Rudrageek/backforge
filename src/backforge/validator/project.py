from pathlib import Path


REQUIRED_FILES = {
    "package.json",
    "prisma/schema.prisma",
    "src/lib/prisma.ts",
}


def validate_generated_project(
    project_path: str,
) -> dict:
    """
    Perform basic structural validation of a
    generated backend project.
    """

    root = Path(project_path)

    if not root.exists():
        return {
            "valid": False,
            "errors": [
                f"Project does not exist: {project_path}"
            ],
        }

    errors = []

    for relative_path in REQUIRED_FILES:
        file_path = root / relative_path

        if not file_path.exists():
            errors.append(
                f"Missing required file: {relative_path}"
            )

    route_files = list(
        (root / "src" / "app").rglob("route.ts")
    ) if (root / "src" / "app").exists() else []

    if not route_files:
        errors.append(
            "No API route files were generated."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "route_count": len(route_files),
    }