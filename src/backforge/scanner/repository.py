from backforge.analyzer.requirements import (
    analyze_requirements,
)

from backforge.scanner.backend import (
    detect_backend,
)

from backforge.analyzer.api_calls import (
    analyze_api_calls_in_project,
)

from backforge.analyzer.backend_routes import (
    analyze_backend_routes,
)

from backforge.analyzer.contract import (
    compare_api_contracts,
)

from backforge.analyzer.forms import (
    analyze_forms_in_project,
)

from backforge.analyzer.intent import (
    infer_form_intent,
)

from backforge.analyzer.routes import (
    detect_nextjs_routes,
)

from backforge.blueprint.application import (
    ApplicationBlueprint,
)

from backforge.scanner.files import (
    find_source_files,
)

from backforge.scanner.package import (
    detect_framework,
    read_package_json,
)


def scan_project(
    project_path: str,
) -> ApplicationBlueprint:
    """
    Scan a frontend repository and create
    an application blueprint.
    """

    files = find_source_files(
        project_path
    )

    backend = detect_backend(
        project_path
    )

    package_data = read_package_json(
        project_path
    )

    framework = detect_framework(
        package_data
    )

    routes = []

    if framework == "Next.js":
        routes = detect_nextjs_routes(
            project_path
        )

    forms = analyze_forms_in_project(
        project_path
    )

    enriched_forms = []

    for form in forms:

        file_path = form.get(
            "file",
            "",
        )

        route = None

        normalized_path = (
            file_path.replace(
                "\\",
                "/",
            )
        )

        if "/login/" in normalized_path:
            route = "/login"

        intent = infer_form_intent(
            form,
            route,
        )

        enriched_form = {
            **form,
            "intent": intent["intent"],
            "confidence": intent["confidence"],
            "evidence": intent["evidence"],
        }

        enriched_forms.append(
            enriched_form
        )

    api_calls = (
        analyze_api_calls_in_project(
            project_path
        )
    )

    backend_routes = (
        analyze_backend_routes(
            project_path
        )
    )

    contract = compare_api_contracts(
        api_calls,
        backend_routes,
    )

    blueprint = ApplicationBlueprint(
        project_path=project_path,
        framework=framework,
        source_file_count=len(files),
        routes=routes,
        forms=enriched_forms,
        api_calls=api_calls,

        backend_detected=backend[
            "detected"
        ],

        backend_indicator_files=backend[
            "indicator_files"
        ],

        backend_indicator_directories=backend[
            "indicator_directories"
        ],

        backend_routes=backend_routes,

        implemented_api_calls=contract[
            "implemented"
        ],

        missing_api_calls=contract[
            "missing"
        ],

        extra_backend_routes=contract[
            "extra"
        ],
    )

    requirements = analyze_requirements(
        blueprint
    )

    blueprint.requirements = requirements

    return blueprint