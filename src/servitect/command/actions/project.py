import re
from design_structure import DesignStructure, Project
from rich.prompt import Prompt
from rich import print

def validate_project_name(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9 ]+$", name)) and len(name.strip()) > 0


def validate_version(version: str) -> bool:
    return bool(re.match(r"^\\d+\\.\\d+\\.\\d+$", version))


def validate_port(port: str) -> bool:
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False


def project(state: DesignStructure) -> None:
    project_data: Project = state.project
    project_name = project_data.name
    project_version = project_data.version
    uvicorn_port = project_data.uvicorn_port

    while True:
        project_name = Prompt.ask(
            "[bold blue]Project name[/bold blue]",
            default=project_name,
            show_default=True,
        )
        if validate_project_name(project_name):
            break
        print(
            "[bold red]Invalid project name. Use alphanumeric characters and spaces only.[/bold red]"
        )

    while True:
        project_version = Prompt.ask(
            "[bold blue]Project version[/bold blue]",
            default=project_version,
            show_default=True,
        )
        if validate_version(project_version):
            break
        print(
            "[bold red]Invalid version format. Use format X.Y.Z (e.g., 1.0.0).[/bold red]"
        )

    while True:
        uvicorn_port = Prompt.ask(
            "[bold blue]Uvicorn port[/bold blue]",
            default=str(uvicorn_port),
            show_default=True,
        )
        if validate_port(uvicorn_port):
            break
        print("[bold red]Invalid port. Use a number between 1 and 65535.[/bold red]")

    project_data.name = project_name
    project_data.version = project_version
    project_data.uvicorn_port = int(uvicorn_port)
