import typer

from backforge.blueprint.builder import (
    build_specification,
)

from backforge.blueprint.planner import (
    build_backend_plan,
)

from backforge.blueprint.session import (
    ConfigurationSession,
)

from backforge.generator.backend import (
    generate_backend,
)

from backforge.scanner.files import (
    find_source_files,
)

from backforge.scanner.repository import (
    scan_project,
)

from backforge.validator.commands import (
    verify_generated_project,
)


app = typer.Typer(
    name="backforge",
    help="Frontend-to-backend architecture and generation platform.",
)


@app.command("scan")
def scan(
    project_path: str = typer.Argument(
        ...,
        help="Path to the frontend project.",
    ),
):
    """Scan a frontend project."""

    print("BackForge")
    print("─────────")
    print(f"Scanning: {project_path}")
    print()

    try:
        files = find_source_files(project_path)

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"Error: {error}")
        raise typer.Exit(code=1)

    print(
        f"Source files found: {len(files)}"
    )
    print()

    for file in files:
        print(f"  {file}")

    print()
    print("Scan complete.")


def ask_configuration_questions(
    session: ConfigurationSession,
) -> None:
    """
    Ask unresolved backend configuration questions
    interactively and apply the user's answers.
    """

    while not session.is_complete():
        questions = session.get_questions()

        if not questions:
            break

        question = questions[0]

        print()
        print(
            f"{question['category'].upper()}"
        )
        print(
            question["question"]
        )
        print()

        options = question.get(
            "options",
            [],
        )

        if not options:
            raise ValueError(
                f"No options available for "
                f"{question['id']}"
            )

        for index, option in enumerate(
            options,
            start=1,
        ):
            print(
                f"  {index}. {option}"
            )

        print()

        while True:
            answer = typer.prompt(
                "Choose an option",
                type=int,
            )

            if 1 <= answer <= len(options):
                break

            print(
                f"Please choose a number "
                f"between 1 and {len(options)}."
            )

        selected_value = options[
            answer - 1
        ]

        session.answer(
            question["id"],
            selected_value,
        )


@app.command("build")
def build(
    project_path: str = typer.Argument(
        ...,
        help="Path to the frontend project.",
    ),
    output_path: str = typer.Option(
        "generated-backend",
        "--output",
        "-o",
        help="Directory for generated backend.",
    ),
):
    """
    Analyze a frontend, configure requirements,
    generate a backend, and verify it.
    """

    print("BackForge")
    print("─────────")
    print()

    print(
        f"Project: {project_path}"
    )

    print()

    # --------------------------------------------------
    # Analysis
    # --------------------------------------------------

    print("Analysis")
    print("────────")

    blueprint = scan_project(
        project_path
    )

    print(
        f"Framework: {blueprint.framework}"
    )

    print(
        f"Routes: {len(blueprint.routes)}"
    )

    print(
        f"API calls: {len(blueprint.api_calls)}"
    )

    print(
        f"Missing APIs: "
        f"{len(blueprint.missing_api_calls)}"
    )

    specification = build_specification(
        blueprint
    )

    print(
        f"Entities: "
        f"{len(specification.entities)}"
    )

    authentication = (
        specification.authentication
        .get("enabled", False)
    )

    print(
        "Authentication: "
        + (
            "detected"
            if authentication
            else "not detected"
        )
    )

    print()

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    session = ConfigurationSession(
        specification
    )

    if not session.is_complete():
        print("Configuration")
        print("─────────────")

        ask_configuration_questions(
            session
        )

        specification = (
            session.specification
        )

        print()
        print(
            "Configuration complete."
        )

    # --------------------------------------------------
    # Backend plan
    # --------------------------------------------------

    plan = build_backend_plan(
        specification
    )

    # --------------------------------------------------
    # Generation
    # --------------------------------------------------

    print()
    print("Generation")
    print("──────────")

    generated_files = generate_backend(
        plan,
        output_path,
    )

    for file in generated_files:
        print(f"  ✓ {file}")

    print()

    # --------------------------------------------------
    # Verification
    # --------------------------------------------------

    print("Verification")
    print("────────────")

    verification = verify_generated_project(
        output_path
    )

    for step in verification["steps"]:
        status = (
            "✓"
            if step["success"]
            else "✗"
        )

        print(
            f"  {status} "
            f"{step['name']}"
        )

    print()

    if not verification["valid"]:
        print(
            "BUILD FAILED"
        )

        for error in verification[
            "errors"
        ]:
            print()
            print(error)

        raise typer.Exit(code=1)

    print(
        "BUILD SUCCESSFUL"
    )


@app.command("version")
def version():
    """Show the BackForge version."""

    print(
        "BackForge v0.1.0"
    )


if __name__ == "__main__":
    app()