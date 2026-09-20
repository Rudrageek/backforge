from dataclasses import dataclass, field


@dataclass
class ApplicationBlueprint:
    """
    Structured representation of a frontend application's
    architecture and backend requirements.
    """

    project_path: str
    framework: str
    source_file_count: int

    routes: list[str] = field(default_factory=list)
    forms: list[dict] = field(default_factory=list)
    api_calls: list[dict] = field(default_factory=list)

    backend_detected: bool = False

    backend_indicator_files: list[str] = field(
        default_factory=list
    )

    backend_indicator_directories: list[str] = field(
        default_factory=list
    )

    backend_routes: list[dict] = field(
        default_factory=list
    )

    implemented_api_calls: list[dict] = field(
        default_factory=list
    )

    missing_api_calls: list[dict] = field(
        default_factory=list
    )

    extra_backend_routes: list[dict] = field(
        default_factory=list
    )


    requirements: dict = field(
    default_factory=dict
)

    
    authentication_required: bool = False
    payments_required: bool = False
    email_required: bool = False
    storage_required: bool = False

    entities: list[str] = field(
        default_factory=list
    )

 