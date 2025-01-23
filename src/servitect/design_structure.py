import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List
import questionary
from dacite import from_dict
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text


@dataclass
class Project:
    name: str = field(default_factory=lambda: "default_project")
    version: str = field(default_factory=lambda: "0.0.1")
    uvicorn_port: int = field(default_factory=lambda: 8000)


@dataclass
class Database:
    url: str = field(default_factory=lambda: "sqlite:///./_data.db")
    migration_dir: str = field(default_factory=lambda: "migrations")


@dataclass
class Security:
    jwt_secret: str = field(default_factory=lambda: "CHANGE_THIS_SECRET")


@dataclass
class ModelField:
    name: str = field(default_factory=lambda: "default_field")
    type: str = field(default_factory=lambda: "str")
    primary: bool = field(default_factory=lambda: False)


@dataclass
class Model:
    fields: List[ModelField] = field(default_factory=list)
    permissions: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class CronJob:
    schedule: str = field(default_factory=lambda: "0 * * * *")
    handler: str = field(default_factory=lambda: "default_handler")


@dataclass
class AIAssistant:
    name: str = field(default_factory=lambda: "assistant1")
    prompt: str = field(default_factory=lambda: "Generic prompt goes here")
    access: List[str] = field(default_factory=lambda: list())


@dataclass
class AI:
    api_key: str = field(default_factory=lambda: "default_api_key")
    base_url: str = field(default_factory=lambda: "https://api.openai.com/v1")
    assistants: List[AIAssistant] = field(default_factory=lambda: list())


@dataclass
class Testing:
    active: bool = field(default_factory=lambda: False)


@dataclass
class DesignStructure:
    project: Project = field(default_factory=Project)
    database: Database = field(default_factory=Database)
    security: Security = field(default_factory=Security)
    actor: Dict[str, Model] = field(default_factory=lambda: dict())
    model: Dict[str, Model] = field(default_factory=lambda: dict())
    cron: Dict[str, CronJob] = field(default_factory=lambda: dict())
    ai: AI = field(default_factory=AI)
    testing: Testing = field(default_factory=Testing)


DESIGN_DEFAULT_STATE: DesignStructure = DesignStructure()
DESIGN_DEFAULT_STATE.actor["admin"] = Model(
    permissions={"read": ["self"], "write": ["admin"]},
    fields=[
        ModelField(name="id", type="str", primary=True),
        ModelField(name="password", type="str", primary=False),
    ],
)

DESIGN_DEFAULT_STATE.actor["user"] = Model(
    permissions={"read": ["self"], "write": ["admin"]},
    fields=[
        ModelField(name="id", type="str", primary=True),
        ModelField(name="username", type="str", primary=False),
        ModelField(name="first_name", type="str", primary=False),
        ModelField(name="last_name", type="str", primary=False),
        ModelField(name="email", type="str", primary=False),
        ModelField(name="password", type="str", primary=False),
    ],
)


def display_design_structure(state: DesignStructure = DESIGN_DEFAULT_STATE) -> None:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    import questionary

    console = Console()

    def section_panel(content, title):
        return Panel(
            content, 
            title=title, 
            border_style="cyan", 
            title_align="left", 
            expand=False
        )

    def highlight_info(label, value):
        return f"[bold cyan]{label}:[/bold cyan] [white]{value}[/white]"

    # Project Configuration
    project_content = "\n".join([
        highlight_info("Name", state.project.name),
        highlight_info("Version", state.project.version),
        highlight_info("Port", state.project.uvicorn_port)
    ])
    console.print(section_panel(project_content, "PROJECT CONFIGURATION"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # Database Configuration
    db_content = "\n".join([
        highlight_info("URL", state.database.url),
        highlight_info("Migration Directory", state.database.migration_dir)
    ])
    console.print(section_panel(db_content, "DATABASE CONFIGURATION"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # Security Configuration
    security_content = highlight_info("JWT Secret", state.security.jwt_secret)
    console.print(section_panel(security_content, "SECURITY"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # Actors
    actors_content = []
    for name, actor in state.actor.items():
        actor_details = [f"[bold green]Actor: {name}[/bold green]"]
        actor_details.append("  [yellow]Fields:[/yellow]")
        actor_details.extend([
            f"    - {field.name} ([italic white]{field.type}[/italic white])" 
            for field in actor.fields
        ])
        actor_details.append("  [yellow]Permissions:[/yellow]")
        actor_details.extend([
            f"    - [cyan]{action}:[/cyan] {', '.join(roles)}" 
            for action, roles in actor.permissions.items()
        ])
        actors_content.append("\n".join(actor_details))
    console.print(section_panel("\n\n".join(actors_content), "ACTORS"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # Models
    models_content = []
    for name, model in state.model.items():
        model_details = [f"[bold green]Model: {name}[/bold green]"]
        model_details.append("  [yellow]Fields:[/yellow]")
        model_details.extend([
            f"    - {field.name} ([italic white]{field.type}[/italic white])" 
            for field in model.fields
        ])
        model_details.append("  [yellow]Permissions:[/yellow]")
        model_details.extend([
            f"    - [cyan]{action}:[/cyan] {', '.join(roles)}" 
            for action, roles in model.permissions.items()
        ])
        models_content.append("\n".join(model_details))
    console.print(section_panel("\n\n".join(models_content), "MODELS"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # Cron Jobs
    if state.cron:
        cron_content = []
        for name, job in state.cron.items():
            job_details = [
                f"[bold green]Job: {name}[/bold green]",
                highlight_info("  Schedule", job.schedule),
                highlight_info("  Handler", job.handler)
            ]
            cron_content.append("\n".join(job_details))
        console.print(section_panel("\n\n".join(cron_content), "CRON JOBS"))
    else:
        console.print(section_panel("[italic red]No cron jobs configured.[/italic red]", "CRON JOBS"))
    questionary.press_any_key_to_continue("Press any key to continue...").ask()

    # AI Configuration
    ai_content = "\n".join([
        highlight_info("API Key", state.ai.api_key),
        highlight_info("Base URL", state.ai.base_url),
        highlight_info("Assistants", len(state.ai.assistants))
    ])
    console.print(section_panel(ai_content, "AI CONFIGURATION"))

    # Testing
    testing_content = highlight_info("Active", state.testing.active)
    console.print(section_panel(testing_content, "TESTING"))

def project_to_dict(project: Project) -> Dict[str, Any]:
    return asdict(project)


def project_from_dict(data: Dict[str, Any]) -> Project:
    return from_dict(data_class=Project, data=data)


def database_to_dict(database: Database) -> Dict[str, Any]:
    return asdict(database)


def database_from_dict(data: Dict[str, Any]) -> Database:
    return from_dict(data_class=Database, data=data)


def security_to_dict(security: Security) -> Dict[str, Any]:
    return asdict(security)


def security_from_dict(data: Dict[str, Any]) -> Security:
    return from_dict(data_class=Security, data=data)


def model_to_dict(model: Model) -> Dict[str, Any]:
    return {
        "fields": [asdict(field) for field in model.fields],
        "permissions": model.permissions,
    }


def model_from_dict(data: Dict[str, Any]) -> Model:
    return Model(
        fields=[
            from_dict(data_class=ModelField, data=field) for field in data["fields"]
        ],
        permissions=data["permissions"],
    )


def cron_to_dict(cron: CronJob) -> Dict[str, Any]:
    return asdict(cron)


def cron_from_dict(data: Dict[str, Any]) -> CronJob:
    return from_dict(data_class=CronJob, data=data)


def ai_to_dict(ai: AI) -> Dict[str, Any]:
    return {
        "api_key": ai.api_key,
        "base_url": ai.base_url,
        "assistants": [asdict(assistant) for assistant in ai.assistants],
    }


def ai_from_dict(data: Dict[str, Any]) -> AI:
    return AI(
        api_key=data["api_key"],
        base_url=data["base_url"],
        assistants=[
            from_dict(data_class=AIAssistant, data=assistant)
            for assistant in data["assistants"]
        ],
    )


def testing_to_dict(testing: Testing) -> Dict[str, Any]:
    return asdict(testing)


def testing_from_dict(data: Dict[str, Any]) -> Testing:
    return from_dict(data_class=Testing, data=data)


def design_structure_to_json(state: DesignStructure) -> str:
    data = {
        "project": project_to_dict(state.project),
        "database": database_to_dict(state.database),
        "security": security_to_dict(state.security),
        "actor": {key: model_to_dict(value) for key, value in state.actor.items()},
        "model": {key: model_to_dict(value) for key, value in state.model.items()},
        "cron": {key: cron_to_dict(value) for key, value in state.cron.items()},
        "ai": ai_to_dict(state.ai),
        "testing": testing_to_dict(state.testing),
    }
    return data


def json_to_design_structure(data: dict) -> DesignStructure:
    return DesignStructure(
        project=project_from_dict(data["project"]),
        database=database_from_dict(data["database"]),
        security=security_from_dict(data["security"]),
        actor={key: model_from_dict(value) for key, value in data["actor"].items()},
        model={key: model_from_dict(value) for key, value in data["model"].items()},
        cron={key: cron_from_dict(value) for key, value in data["cron"].items()},
        ai=ai_from_dict(data["ai"]),
        testing=testing_from_dict(data["testing"]),
    )
