import questionary
from design_structure import DesignStructure, AIAssistant
from rich import print
from questionary import ValidationError


def ai(design_structure: DesignStructure) -> None:
    ai_data = design_structure.ai

    def validate_name(value):
        """Validate unique assistant name."""
        if any(assistant.name == value for assistant in ai_data.assistants):
            raise ValidationError(message="Assistant with this name already exists")
        return value

    while True:
        action = questionary.select(
            "Select an action",
            choices=[
                "Edit API Key and Base URL",
                "Edit Assistants",
                "Exit",
            ],
            use_arrow_keys=True,
        ).ask()

        if action == "Edit API Key and Base URL":
            api_key = questionary.text(
                "Enter the API Key", default=ai_data.api_key
            ).ask()
            base_url = questionary.text(
                "Enter the Base URL", default=ai_data.base_url
            ).ask()
            ai_data.api_key = api_key
            ai_data.base_url = base_url
        elif action == "Edit Assistants":
            while True:
                assistant_action = questionary.select(
                    "Select an action",
                    choices=[
                        "Add a new Assistant",
                        "Edit an existing Assistant",
                        "Delete an Assistant",
                        "Exit",
                    ],
                    use_arrow_keys=True,
                ).ask()

                if assistant_action == "Add a new Assistant":
                    name = questionary.text(
                        "Enter the name for the new Assistant", validate=validate_name
                    ).ask()

                    if not design_structure.actor:
                        print(
                            "[bold red]No actors available, cannot add assistant[/bold red]"
                        )
                        continue

                    prompt = questionary.text(
                        "Enter the prompt for the new Assistant"
                    ).ask()

                    access = questionary.select(
                        "Select actors to give access to",
                        choices=[actor for actor in design_structure.actor.keys()],
                    ).ask()

                    ai_data.assistants.append(
                        AIAssistant(name=name, prompt=prompt, access=[access])
                    )
                elif assistant_action == "Edit an existing Assistant":
                    assistants = [
                        (assistant.name, assistant) for assistant in ai_data.assistants
                    ]
                    if not assistants:
                        print("[bold red]No assistants to edit[/bold red]")
                        continue
                    assistant_name = questionary.select(
                        "Select an assistant to edit",
                        choices=[name for name, _ in assistants],
                    ).ask()

                    assistant = next(
                        (
                            assistant
                            for name, assistant in assistants
                            if name == assistant_name
                        ),
                        None,
                    )

                    if assistant is None:
                        print("[bold red]Invalid selection[/bold red]")
                        continue
                    if not design_structure.actor:
                        print(
                            "[bold red]No actors available, cannot edit assistant[/bold red]"
                        )
                        continue

                    name = questionary.text(
                        "Enter the new name for the assistant",
                        default=assistant.name,
                    ).ask()
                    prompt = questionary.text(
                        "Enter the new prompt for the assistant",
                        default=assistant.prompt,
                    ).ask()
                    access = questionary.autocomplete(
                        "Select actors to give access to",
                        choices=[actor for actor in design_structure.actor.keys()],
                        default=assistant.access,
                    ).ask()

                    assistant.name = name
                    assistant.prompt = prompt
                    assistant.access = [access]
                elif assistant_action == "Delete an Assistant":
                    assistants = [
                        (assistant.name, assistant) for assistant in ai_data.assistants
                    ]
                    if not assistants:
                        print("[bold red]No assistants to delete[/bold red]")
                        continue
                    assistant_name = questionary.autocomplete(
                        "Select an assistant to delete",
                        choices=[name for name, _ in assistants],
                    ).ask()

                    assistant = next(
                        (
                            assistant
                            for name, assistant in assistants
                            if name == assistant_name
                        ),
                        None,
                    )

                    if assistant is None:
                        print("[bold red]Invalid selection[/bold red]")
                        continue
                    ai_data.assistants.remove(assistant)
                else:
                    break
        else:
            break
