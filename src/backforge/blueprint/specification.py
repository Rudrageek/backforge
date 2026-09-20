from dataclasses import dataclass, field


@dataclass
class BackendSpecification:
    """
    User-approved configuration for the backend
    BackForge is expected to build.
    """

    authentication: dict = field(
        default_factory=dict
    )

    database: dict = field(
        default_factory=dict
    )

    payments: dict = field(
        default_factory=dict
    )

    email: dict = field(
        default_factory=dict
    )

    storage: dict = field(
        default_factory=dict
    )

    api: dict = field(
        default_factory=lambda: {
            "required": [],
            "missing": [],
            "request_bodies": [],
        }
    )

    entities: list[dict] = field(
        default_factory=list
    )