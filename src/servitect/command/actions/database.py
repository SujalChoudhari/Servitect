import questionary
from design_structure import DesignStructure
from rich import print

def validate_url(url: str) -> bool:
    return True if url.startswith("sqlite://") else False

def database(design_structure: DesignStructure) -> None:
    database_data = design_structure.database

    while True:
        database_url = questionary.text(
            "Enter the database URL",
            default=database_data.url
        ).ask()

        if database_url is None:
            print("[bold red]Operation cancelled by user.[/bold red]")
            return

        if validate_url(database_url):
            database_data.url = database_url
            break
        print("[bold red]Invalid database URL.[/bold red]")

    while True:
        migration_dir = questionary.text(
            "Enter the migration directory",
            default=database_data.migration_dir
        ).ask()

        if migration_dir is None:
            print("[bold red]Operation cancelled by user.[/bold red]")
            return

        if migration_dir:
            database_data.migration_dir = migration_dir
            break
        print("[bold red]Invalid migration directory.[/bold red]")

    design_structure.database = database_data
