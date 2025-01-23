import questionary
from design_structure import DesignStructure
from rich import print


def testing(design_structure: DesignStructure) -> None:
    testing_data = design_structure.testing

    # Ask if the user wants to enable testing
    action = questionary.select(
        "Do you want to enable testing?",
        choices=["Yes", "No"],
        default="Yes"
    ).ask()

    # Set the active testing flag based on user input
    testing_data.active = action == "Yes"

    if testing_data.active:
        print("[bold green]Testing enabled.[/bold green]")
    else:
        print("[bold red]Testing disabled.[/bold red]")

    # Update the design_structure with the new testing data
    design_structure.testing = testing_data
