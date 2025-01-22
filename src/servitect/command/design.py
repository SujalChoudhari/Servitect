import inquirer
import copy

from command.actions.actor import actor
from command.actions.ai import ai
from command.actions.cron import cron
from command.actions.project import project
from command.actions.security import security
from design_structure import (
    DESIGN_DEFAULT_STATE,
    DesignStructure,
    json_to_design_structure,
    design_structure_to_json,
    display_design_structure,
)
import json
import os
import rich

current_state: DesignStructure = None


def design() -> None:
    global current_state
    schema_file = "servitect.schema.json"
    if os.path.exists(schema_file):
        with open(schema_file, "r") as f:
            current_state = json_to_design_structure(json.loads(f.read()))
    else:
        current_state = copy.deepcopy(DESIGN_DEFAULT_STATE)
        with open(schema_file, "w") as f:
            f.write(json.dumps(design_structure_to_json(current_state),indent=4))
    while True:
        show_menu()
        rich.print("[bold green]Saved changes![/bold green]")
        with open(schema_file, "w") as f:
            f.write(json.dumps(design_structure_to_json(current_state),indent=4))


def show_menu() -> None:
    """Show a menu for user to select."""
    questions = [
        inquirer.List(
            "action",
            message="Select an action",
            choices=[
                "View",
                "Project",
                "Database",
                "Security",
                "Actor",
                "Model",
                "Cron",
                "AI",
                "Testing",
                "Exit",
            ],
            carousel=True,
        ),
    ]

    answers = inquirer.prompt(questions)
    action = answers["action"]

    functions = {
        "View": view,
        "Project": project,
        "Database": database,
        "Security": security,
        "Actor": actor,
        "Model": model,
        "Cron": cron,
        "AI": ai,
        "Testing": testing,
        "Exit": terminate,
    }

    if action in functions:
        functions[action](current_state)
    else:
        print("Invalid selection")


def view(current_state: DesignStructure) -> None:
    display_design_structure(current_state)
    input("Press Enter to continue...")


def terminate(_: DesignStructure) -> None:
    raise SystemExit()


def database():
    pass


def model():
    pass


def testing():
    pass


def exit():
    pass
