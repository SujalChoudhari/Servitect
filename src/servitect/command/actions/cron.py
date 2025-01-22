import inquirer
from rich import print
from design_structure import DesignStructure, CronJob


def cron(design_structure: DesignStructure) -> None:
    cron_data = design_structure.cron

    questions = [
        inquirer.List(
            "action",
            message="Select an action",
            choices=[
                "Add a new cron job",
                "Edit an existing cron job",
                "Delete a cron job",
                "Exit",
            ],
            carousel=True,
        ),
    ]

    while True:
        answers = inquirer.prompt(questions)
        action = answers["action"]

        if action == "Add a new cron job":
            schedule = inquirer.text(
                message="Enter the schedule for the new cron job (see https://crontab.guru/ for help)",
                default="0 * * * *",
            )
            handler = inquirer.text(
                message="Enter the name for the new cron job (services.example_handler)",
                default="services.example_handler",
            )
            if handler not in cron_data:
                cron_data[handler] = CronJob(schedule=schedule, handler=handler)
            else:
                print("[bold red]Cron job with this handler already exists.[/bold red]")
        elif action == "Edit an existing cron job":
            handlers = list(cron_data.keys())
            if not handlers:
                print("[bold red]No cron jobs to edit[/bold red]")
                continue
            handler = inquirer.list_input(
                "Select a cron job to edit",
                choices=handlers,
            )
            if handler not in cron_data:
                print("[bold red]Invalid selection[/bold red]")
                continue
            schedule = inquirer.text(
                message="Enter the new schedule for the cron job (see https://crontab.guru/ for help)",
                default=cron_data[handler].schedule,
            )
            handler_name = inquirer.text(
                message="Enter the new name for the cron job", default=handler
            )
            if handler_name not in cron_data or handler == handler_name:
                cron_data[handler_name] = CronJob(
                    schedule=schedule, handler=handler_name
                )
                if handler != handler_name:
                    del cron_data[handler]
            else:
                print(
                    "[bold red]Cron job with the new handler name already exists.[/bold red]"
                )
        elif action == "Delete a cron job":
            handlers = list(cron_data.keys())
            if not handlers:
                print("[bold red]No cron jobs to delete[/bold red]")
                continue
            handler = inquirer.list_input(
                "Select a cron job to delete",
                choices=handlers,
            )
            if handler in cron_data:
                del cron_data[handler]
            else:
                print("[bold red]Invalid selection[/bold red]")
        elif action == "Exit":
            break
        else:
            print("[bold red]Invalid selection[/bold red]")
