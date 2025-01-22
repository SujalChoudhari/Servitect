import inquirer
from design_structure import DesignStructure, AIAssistant
from rich import print


def ai(design_structure: DesignStructure) -> None:
    ai_data = design_structure.ai

    while True:
        questions = [
            inquirer.List(
                "action",
                message="Select an action",
                choices=[
                    "Edit API Key and Base URL",
                    "Edit Assistants",
                    "Exit",
                ],
                carousel=True,
            ),
        ]

        answers = inquirer.prompt(questions)
        action = answers["action"]

        if action == "Edit API Key and Base URL":
            api_key = inquirer.text(
                message="Enter the API Key", default=ai_data.api_key
            )
            base_url = inquirer.text(
                message="Enter the Base URL", default=ai_data.base_url
            )
            ai_data.api_key = api_key
            ai_data.base_url = base_url
        elif action == "Edit Assistants":
            while True:
                questions = [
                    inquirer.List(
                        "action",
                        message="Select an action",
                        choices=[
                            "Add a new Assistant",
                            "Edit an existing Assistant",
                            "Delete an Assistant",
                            "Exit",
                        ],
                        carousel=True,
                    ),
                ]

                answers = inquirer.prompt(questions)
                action = answers["action"]

                if action == "Add a new Assistant":
                    name = inquirer.text(
                        message="Enter the name for the new Assistant"
                    )
                    if any(assistant.name == name for assistant in ai_data.assistants):
                        print("[bold red]Assistant with this name already exists[/bold red]")
                        continue
                    if not design_structure.actor:
                        print("[bold red]No actors available, cannot add assistant[/bold red]")
                        continue
                    prompt = inquirer.text(
                        message="Enter the prompt for the new Assistant"
                    )
                    access = inquirer.checkbox(
                        message="Select actors to give access to",
                        choices=list(design_structure.actor.keys()),
                    )
                    ai_data.assistants.append(
                        AIAssistant(name=name, prompt=prompt, access=access)
                    )
                elif action == "Edit an existing Assistant":
                    assistants = [
                        (assistant.name, assistant)
                        for assistant in ai_data.assistants
                    ]
                    if not assistants:
                        print("[bold red]No assistants to edit[/bold red]")
                        continue
                    assistant_name = inquirer.list_input(
                        "Select an assistant to edit", choices=[name for name, _ in assistants]
                    )
                    assistant = next(
                        (assistant for name, assistant in assistants if name == assistant_name), None
                    )
                    if assistant is None:
                        print("[bold red]Invalid selection[/bold red]")
                        continue
                    if not design_structure.actor:
                        print("[bold red]No actors available, cannot edit assistant[/bold red]")
                        continue
                    name = inquirer.text(
                        message="Enter the new name for the assistant",
                        default=assistant.name,
                    )
                    prompt = inquirer.text(
                        message="Enter the new prompt for the assistant",
                        default=assistant.prompt,
                    )
                    access = inquirer.checkbox(
                        message="Select actors to give access to",
                        choices=list(design_structure.actor.keys()),
                        default=assistant.access,
                    )
                    assistant.name = name
                    assistant.prompt = prompt
                    assistant.access = access
                elif action == "Delete an Assistant":
                    assistants = [
                        (assistant.name, assistant)
                        for assistant in ai_data.assistants
                    ]
                    if not assistants:
                        print("[bold red]No assistants to delete[/bold red]")
                        continue
                    assistant_name = inquirer.list_input(
                        "Select an assistant to delete", choices=[name for name, _ in assistants]
                    )
                    assistant = next(
                        (assistant for name, assistant in assistants if name == assistant_name), None
                    )
                    if assistant is None:
                        print("[bold red]Invalid selection[/bold red]")
                        continue
                    ai_data.assistants.remove(assistant)
                else:
                    break
        else:
            break
