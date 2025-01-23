import re
from design_structure import DesignStructure, Project
from rich import print
import questionary

def validate_project_name(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9 ]+$", name)) and len(name.strip()) > 0

def validate_version(version: str) -> bool:
    if(version.count(".") > 2):
        return False
    return True if [x for x in version.split(".") if x.isdigit()] == version.split(".") else False

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
        project_name = questionary.text(
            "Project name",
            default=project_name,
        ).ask()

        if project_name is None:
            print("[bold red]Operation cancelled by user.[/bold red]")
            return

        if validate_project_name(project_name):
            break
        print(
            "[bold red]Invalid project name. Use alphanumeric characters and spaces only.[/bold red]"
        )

    while True:
        project_version = questionary.text(
            "Project version",
            default=project_version,
        ).ask()

        if project_version is None:
            print("[bold red]Operation cancelled by user.[/bold red]")
            return

        if validate_version(project_version):
            break
        print(
            "[bold red]Invalid version format. Use format X.Y.Z (e.g., 1.0.0).[/bold red]"
        )

    while True:
        uvicorn_port = questionary.text(
            "Uvicorn port",
            default=str(uvicorn_port),
        ).ask()

        if uvicorn_port is None:
            print("[bold red]Operation cancelled by user.[/bold red]")
            return

        if validate_port(uvicorn_port):
            break
        print("[bold red]Invalid port. Use a number between 1 and 65535.[/bold red]")

    project_data.name = project_name
    project_data.version = project_version
    project_data.uvicorn_port = int(uvicorn_port)

