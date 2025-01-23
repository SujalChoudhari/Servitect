import questionary
from rich import print
from design_structure import DesignStructure, CronJob

def cron(design_structure: DesignStructure) -> None:
    cron_data = design_structure.cron

    while True:
        action = questionary.select(
            "Select an action",
            choices=[
                "Add a new cron job",
                "Edit an existing cron job",
                "Delete a cron job",
                "Exit",
            ],
        ).ask()

        if action is None or action == "Exit":
            break

        if action == "Add a new cron job":
            schedule_type = questionary.select(
                "Choose a schedule type",
                choices=[
                    "Every minute",
                    "Every 15 minutes",
                    "Every hour",
                    "Daily at midnight",
                    "Weekly on Sunday",
                    "Monthly",
                    "Yearly",
                    "Custom",
                ],
            ).ask()

            schedule_map = {
                "Every minute": "* * * * *",
                "Every 15 minutes": "*/15 * * * *",
                "Every hour": "0 * * * *",
                "Daily at midnight": "0 0 * * *",
                "Weekly on Sunday": "0 0 * * 0",
                "Monthly": "0 0 1 * *",
                "Yearly": "0 0 1 1 *",
            }

            if schedule_type == "Custom":
                schedule = questionary.text(
                    "Enter a custom schedule (e.g., cron pattern: '0 0 * * *')",
                    validate=lambda text: text.strip() != "",
                ).ask()
            else:
                schedule = schedule_map.get(schedule_type, "")

            handler = questionary.autocomplete(
                "Enter the name for the new cron job",
                choices=[
                    "services.example_handler",
                    "services.cleanup",
                    "services.email_notification",
                    "services.backup",
                ],
            ).ask()

            if not schedule or not handler:
                print("[bold red]Invalid input. Both schedule and handler are required.[/bold red]")
                continue

            if handler not in cron_data:
                cron_data[handler] = CronJob(schedule=schedule, handler=handler)
            else:
                print("[bold red]Cron job with this handler already exists.[/bold red]")

        elif action == "Edit an existing cron job":
            handlers = list(cron_data.keys())
            if not handlers:
                print("[bold red]No cron jobs to edit.[/bold red]")
                continue

            handler = questionary.autocomplete(
                "Select a cron job to edit",
                choices=handlers,
            ).ask()

            if not handler or handler not in cron_data:
                print("[bold red]Invalid selection.[/bold red]")
                continue

            schedule_type = questionary.select(
                "Choose a new schedule type",
                choices=[
                    "Every minute",
                    "Every 15 minutes",
                    "Every hour",
                    "Daily at midnight",
                    "Weekly on Sunday",
                    "Monthly",
                    "Yearly",
                    "Custom",
                ],
            ).ask()

            if schedule_type == "Custom":
                schedule = questionary.text(
                    "Enter a custom schedule (e.g., cron pattern: '0 0 * * *')",
                    default=cron_data[handler].schedule,
                    validate=lambda text: text.strip() != "",
                ).ask()
            else:
                schedule_map = {
                    "Every minute": "* * * * *",
                    "Every 15 minutes": "*/15 * * * *",
                    "Every hour": "0 * * * *",
                    "Daily at midnight": "0 0 * * *",
                    "Weekly on Sunday": "0 0 * * 0",
                    "Monthly": "0 0 1 * *",
                    "Yearly": "0 0 1 1 *",
                }
                schedule = schedule_map.get(schedule_type, cron_data[handler].schedule)

            new_handler = questionary.autocomplete(
                "Enter the new name for the cron job",
                choices=[
                    "services.example_handler",
                    "services.cleanup",
                    "services.email_notification",
                    "services.backup",
                ],
                default=handler,
            ).ask()

            if not schedule or not new_handler:
                print("[bold red]Invalid input. Both schedule and handler are required.[/bold red]")
                continue

            if new_handler not in cron_data or handler == new_handler:
                cron_data[new_handler] = CronJob(schedule=schedule, handler=new_handler)
                if handler != new_handler:
                    del cron_data[handler]
            else:
                print("[bold red]Cron job with the new handler name already exists.[/bold red]")

        elif action == "Delete a cron job":
            handlers = list(cron_data.keys())
            if not handlers:
                print("[bold red]No cron jobs to delete.[/bold red]")
                continue

            handler = questionary.autocomplete(
                "Select a cron job to delete",
                choices=handlers,
            ).ask()

            if handler in cron_data:
                del cron_data[handler]
            else:
                print("[bold red]Invalid selection.[/bold red]")