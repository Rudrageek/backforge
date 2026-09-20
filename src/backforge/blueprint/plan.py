from dataclasses import dataclass, field


@dataclass
class BackendPlan:
    database: dict = field(default_factory=dict)
    api: list[dict] = field(default_factory=list)
    authentication: dict = field(default_factory=dict)
    integrations: list[dict] = field(default_factory=list)