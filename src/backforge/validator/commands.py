import subprocess
from pathlib import Path


def run_command(
    command: list[str],
    project_path: str,
) -> dict:
    result = subprocess.run(
        command,
        cwd=project_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "success": result.returncode == 0,
        "stdout": (result.stdout or "").strip(),
        "stderr": (result.stderr or "").strip(),
    }


def verify_generated_project(
    project_path: str,
) -> dict:
    root = Path(project_path)

    if not root.exists():
        return {
            "valid": False,
            "steps": [],
            "errors": [
                f"Project does not exist: {project_path}"
            ],
        }

    steps = []

    # --------------------------------------------------
    # Install dependencies
    # --------------------------------------------------

    package_json = root / "package.json"

    if package_json.exists():
        install_result = run_command(
            ["npm", "install"],
            project_path,
        )

        steps.append(
            {
                "name": "npm_install",
                **install_result,
            }
        )

        if not install_result["success"]:
            return {
                "valid": False,
                "steps": steps,
                "errors": [
                    install_result["stderr"]
                    or install_result["stdout"]
                ],
            }

    # --------------------------------------------------
    # Prisma
    # --------------------------------------------------

    prisma_result = run_command(
        ["npx", "prisma", "generate"],
        project_path,
    )

    steps.append(
        {
            "name": "prisma_generate",
            **prisma_result,
        }
    )

    if not prisma_result["success"]:
        return {
            "valid": False,
            "steps": steps,
            "errors": [
                prisma_result["stderr"]
                or prisma_result["stdout"]
            ],
        }

    # --------------------------------------------------
    # TypeScript
    # --------------------------------------------------

    typescript_result = run_command(
        ["npx", "tsc", "--noEmit"],
        project_path,
    )

    steps.append(
        {
            "name": "typescript",
            **typescript_result,
        }
    )

    errors = []

    if not typescript_result["success"]:
        errors.append(
            typescript_result["stderr"]
            or typescript_result["stdout"]
        )

    return {
        "valid": len(errors) == 0,
        "steps": steps,
        "errors": errors,
    }