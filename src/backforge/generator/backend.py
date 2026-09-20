from pathlib import Path

from backforge.generator.auth import generate_register_route
from backforge.generator.auth_login import generate_login_route
from backforge.generator.next_api import generate_next_api_route
from backforge.generator.package_json import generate_package_json
from backforge.generator.prisma import generate_prisma_schema
from backforge.generator.prisma_client import generate_prisma_client
from backforge.generator.prisma_config import generate_prisma_config
from backforge.generator.tsconfig import generate_tsconfig
from backforge.generator.writer import write_generated_file


def generate_backend(plan, output_root: str) -> list[Path]:
    generated_files = []

    # --------------------------------------------------
    # Package
    # --------------------------------------------------

    package_json = generate_package_json()

    generated_files.append(
        write_generated_file(
            output_root,
            "package.json",
            package_json,
        )
    )

    # --------------------------------------------------
    # TypeScript
    # --------------------------------------------------

    tsconfig = generate_tsconfig()

    generated_files.append(
        write_generated_file(
            output_root,
            "tsconfig.json",
            tsconfig,
        )
    )

    # --------------------------------------------------
    # Prisma
    # --------------------------------------------------

    prisma_schema = generate_prisma_schema(
        plan.database
    )

    generated_files.append(
        write_generated_file(
            output_root,
            "prisma/schema.prisma",
            prisma_schema,
        )
    )

    prisma_config = generate_prisma_config()

    generated_files.append(
        write_generated_file(
            output_root,
            "prisma.config.ts",
            prisma_config,
        )
    )

    prisma_client = generate_prisma_client()

    generated_files.append(
        write_generated_file(
            output_root,
            "src/lib/prisma.ts",
            prisma_client,
        )
    )

    # --------------------------------------------------
    # API routes
    # --------------------------------------------------

    models = plan.database.get("models", [])

    model_name = (
        models[0]["name"]
        if models
        else None
    )

    for api in plan.api:

        if not model_name:
            continue

        endpoint = api.get("endpoint")

        if not endpoint:
            continue

        route = generate_next_api_route(
            api,
            model_name,
        )

        route_directory = (
            Path("src")
            / "app"
            / endpoint.strip("/")
        )

        generated_files.append(
            write_generated_file(
                output_root,
                str(route_directory / "route.ts"),
                route,
            )
        )

    # --------------------------------------------------
    # Authentication
    # --------------------------------------------------

    authentication = plan.authentication

    if (
        authentication.get("enabled")
        and authentication.get("method")
        == "email_password"
    ):
        # Register
        register_route = generate_register_route()

        generated_files.append(
            write_generated_file(
                output_root,
                "src/app/api/auth/register/route.ts",
                register_route,
            )
        )

        # Login
        login_route = generate_login_route()

        generated_files.append(
            write_generated_file(
                output_root,
                "src/app/api/auth/login/route.ts",
                login_route,
            )
        )

    return generated_files