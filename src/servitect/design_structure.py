import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

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
class ActorField:
    name: str = field(default_factory=lambda: "default_field")
    type: str = field(default_factory=lambda: "str")
    primary: bool = field(default_factory=lambda: False)


@dataclass
class Actor:
    fields: List[ActorField] = field(default_factory=list)
    permissions: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class Model:
    fields: List[ActorField] = field(default_factory=list)
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
    actor: Dict[str, Actor] = field(default_factory=lambda: dict())
    model: Dict[str, Model] = field(default_factory=lambda: dict())
    cron: Dict[str, CronJob] = field(default_factory=lambda: dict())
    ai: AI = field(default_factory=AI)
    testing: Testing = field(default_factory=Testing)


DESIGN_DEFAULT_STATE: DesignStructure = DesignStructure()
DESIGN_DEFAULT_STATE.actor["admin"] = Actor(
    permissions={"read": ["self"], "write": ["admin"]},
    fields=[
        ActorField(name="id", type="str", primary=True),
        ActorField(name="password", type="str", primary=False),
    ],
)

DESIGN_DEFAULT_STATE.actor["user"] = Actor(
    permissions={"read": ["self"], "write": ["admin"]},
    fields=[
        ActorField(name="id", type="str", primary=True),
        ActorField(name="username", type="str", primary=False),
        ActorField(name="first_name", type="str", primary=False),
        ActorField(name="last_name", type="str", primary=False),
        ActorField(name="email", type="str", primary=False),
        ActorField(name="password", type="str", primary=False),
    ],
)


def display_design_structure(state: DesignStructure = DESIGN_DEFAULT_STATE) -> None:
    console = Console()
    layout = Layout()

    # Split into main sections
    layout.split_column(Layout(name="header", size=3), Layout(name="main", ratio=4))

    # Split main section into three columns
    layout["main"].split_row(
        Layout(name="config", ratio=1),
        Layout(name="entities", ratio=2),
        Layout(name="services", ratio=1),
    )

    # Header with title
    layout["header"].update(
        Panel(Text("Design Structure Dashboard", style="bold magenta"), box=box.HEAVY)
    )

    # Helper function for creating panels
    def create_panel(title: str, content: str) -> Panel:
        return Panel(
            Text.from_markup(content),
            title=f"[bold magenta]{title}[/bold magenta]",
            box=box.ROUNDED,
            border_style="blue",
        )

    # Configuration section (left column)
    config_panels = []

    # Project config
    project_content = "\n".join(
        [
            f"[cyan]Name:[/cyan] {state.project.name}",
            f"[cyan]Version:[/cyan] {state.project.version}",
            f"[cyan]Port:[/cyan] {state.project.uvicorn_port}",
        ]
    )
    config_panels.append(create_panel("Project", project_content))

    # Database config
    db_content = "\n".join(
        [
            f"[cyan]URL:[/cyan] {state.database.url}",
            f"[cyan]Migrations:[/cyan] {state.database.migration_dir}",
        ]
    )
    config_panels.append(create_panel("Database", db_content))

    # Security config
    security_content = f"[cyan]JWT Secret:[/cyan] {state.security.jwt_secret}"
    config_panels.append(create_panel("Security", security_content))

    # Testing config
    testing_content = f"[cyan]Active:[/cyan] {state.testing.active}"
    config_panels.append(create_panel("Testing", testing_content))

    layout["main"]["config"].update(Columns([*config_panels], equal=True))

    # Entities section (middle column)
    entity_panels = []

    # Actors
    for name, actor in state.actor.items():
        fields = "\n".join(
            [
                f"[cyan]{field.name}[/cyan] ([white]{field.type}[/white]"
                + f"{' [yellow]PRIMARY[/yellow]' if field.primary else ''})"
                for field in actor.fields
            ]
        )
        perms = "\n".join(
            [
                f"[cyan]{action}:[/cyan] {', '.join(roles)}"
                for action, roles in actor.permissions.items()
            ]
        )
        content = (
            f"[bold]Fields:[/bold]\n{fields}\n\n[bold]Permissions:[/bold]\n{perms}"
        )
        entity_panels.append(create_panel(f"Actor: {name}", content))

    # Models
    for name, model in state.model.items():
        fields = "\n".join(
            [
                f"[cyan]{field.name}[/cyan] ([white]{field.type}[/white]"
                + f"{' [yellow]PRIMARY[/yellow]' if field.primary else ''})"
                for field in model.fields
            ]
        )
        perms = "\n".join(
            [
                f"[cyan]{action}:[/cyan] {', '.join(roles)}"
                for action, roles in model.permissions.items()
            ]
        )
        content = (
            f"[bold]Fields:[/bold]\n{fields}\n\n[bold]Permissions:[/bold]\n{perms}"
        )
        entity_panels.append(create_panel(f"Model: {name}", content))

    layout["main"]["entities"].update(Columns([*entity_panels], equal=True))

    # Services section (right column)
    service_panels = []

    # AI Configuration
    ai_content = "\n".join(
        [
            f"[cyan]API Key:[/cyan] {state.ai.api_key}",
            f"[cyan]Base URL:[/cyan] {state.ai.base_url}",
        ]
    )
    for assistant in state.ai.assistants:
        ai_content += f"\n\n[bold]Assistant: {assistant.name}[/bold]"
        ai_content += f"\n[cyan]Prompt:[/cyan] {assistant.prompt}"
        ai_content += f"\n[cyan]Access:[/cyan] {', '.join(assistant.access)}"
    service_panels.append(create_panel("AI Configuration", ai_content))

    # Cron Jobs
    for name, job in state.cron.items():
        cron_content = "\n".join(
            [
                f"[cyan]Schedule:[/cyan] {job.schedule}",
                f"[cyan]Handler:[/cyan] {job.handler}",
            ]
        )
        service_panels.append(create_panel(f"Cron: {name}", cron_content))

    layout["main"]["services"].update(Columns([*service_panels], equal=True))

    # Display the complete dashboard
    console.print(layout)


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


def actor_to_dict(actor: Actor) -> Dict[str, Any]:
    return {
        "fields": [asdict(field) for field in actor.fields],
        "permissions": actor.permissions,
    }


def actor_from_dict(data: Dict[str, Any]) -> Actor:
    return Actor(
        fields=[
            from_dict(data_class=ActorField, data=field) for field in data["fields"]
        ],
        permissions=data["permissions"],
    )


def model_to_dict(model: Model) -> Dict[str, Any]:
    return {
        "fields": [asdict(field) for field in model.fields],
        "permissions": model.permissions,
    }


def model_from_dict(data: Dict[str, Any]) -> Model:
    return Model(
        fields=[
            from_dict(data_class=ActorField, data=field) for field in data["fields"]
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
        "actor": {key: actor_to_dict(value) for key, value in state.actor.items()},
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
        actor={key: actor_from_dict(value) for key, value in data["actor"].items()},
        model={key: model_from_dict(value) for key, value in data["model"].items()},
        cron={key: cron_from_dict(value) for key, value in data["cron"].items()},
        ai=ai_from_dict(data["ai"]),
        testing=testing_from_dict(data["testing"]),
    )
