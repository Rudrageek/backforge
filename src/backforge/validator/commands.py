import subprocess
from pathlib import Path


def run_command(
    command: list[str],
    project_path: str,
) -> dict:
    """
    Run a command inside the generated project
    and capture its result.
    """

    result = subprocess.run(
        command,
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def verify_generated_project(
    project_path: str,
) -> dict:
    """
    Run Prisma generation and TypeScript
    validation against the generated backend.
    """

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
    # Prisma generation
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
    # TypeScript validation
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