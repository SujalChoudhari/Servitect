import argparse

from rich.console import Console
from rich.panel import Panel
from command.design import design

parser = argparse.ArgumentParser(description="Servitect CLI")
subparsers = parser.add_subparsers(dest="command")

design_parser = subparsers.add_parser(
    "design",
    help="Generate a service design from a YAML file",
    description="Generate a service design from a YAML file",
)

build_parser = subparsers.add_parser(
    "build",
    help="Create a service from a design",
    description="Create a service from a design",
)


def cli():
    args = parser.parse_args()

    console = Console()
    # try:
    if not args.command:
        panel = "[bold green]Welcome to Servitect![/bold green]\n\nServitect is a tool for designing and building microservices.\n\nUse the [bold]design[/bold] command to generate a service design from a YAML file.\n\nUse the [bold]build[/bold] command to create a service from a design.\n\n"
        console.print(Panel(panel, title="Servitect", width=60))
        parser.print_help()
    elif args.command == "design":
        design()
    elif args.command == "build":
        # build()
        pass
    else:
        parser.print_help()
    # except KeyboardInterrupt:
    #     console.print("\n[bold blue]Exiting...[/bold blue]", justify="left")
    # except Exception as e:
    #     console.print(f"[bold red]{e}[/bold red]", justify="left")
        


