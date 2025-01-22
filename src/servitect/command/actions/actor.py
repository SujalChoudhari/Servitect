import inquirer
from design_structure import DesignStructure, ActorField, Actor


def actor(design_structure: DesignStructure) -> None:
    actor_data = design_structure.actor

    while True:
        questions = [
            inquirer.List(
                "action",
                message="Select an action",
                choices=[
                    "Create a new Actor",
                    "Edit an existing Actor",
                    "Delete an Actor",
                    "Exit",
                ],
                carousel=True,
            ),
        ]

        answers = inquirer.prompt(questions)
        action = answers["action"]

        if action == "Create a new Actor":
            name = inquirer.text(message="Enter the Actor name")
            field_names = [
                "id",       # Compulsory field
                "username",
                "first_name",
                "last_name",
                "email",
                "password",
                "date_of_birth",
                "created_at",
                "updated_at"
            ]
            field_types = [
                "int",   # Compulsory field
                "str",
                "str",
                "str",
                "str",
                "str",
                "date",
                "datetime",
                "datetime"
            ]
            field_choices = [
                f"{name} ({field_type})" for name, field_type in zip(field_names, field_types)
            ]
            fields = inquirer.checkbox(
                message="Select the fields to add to the Actor",
                choices=field_choices,
                default=[field_names[0]]
            )

            permissions = {}
            for field in fields:
                permission = inquirer.list_input(
                    message=f"Select the permission level for {field}",
                    choices=["self", "admin", "public"]
                )
                permissions[field] = [permission]


            new_actor = Actor(
                name=name,
                fields=[ActorField(name=field, type=field_type) for field, field_type in zip(fields, field_types)],
                permissions=permissions
            )
            actor_data[name] = new_actor
        elif action == "Edit an existing Actor":
            names = list(actor_data.keys())
            name = inquirer.list_input(
                message="Select the Actor to edit",
                choices=names
            )
            actor_to_edit = actor_data[name]
            while True:
                questions = [
                    inquirer.List(
                        "action",
                        message="Select an action",
                        choices=[
                            "Add a field",
                            "Edit a field",
                            "Delete a field",
                            "Edit permissions",
                            "Exit",
                        ],
                        carousel=True,
                    ),
                ]
                answers = inquirer.prompt(questions)
                action = answers["action"]

                if action == "Add a field":
                    field_name = inquirer.text(message="Enter the field name")
                    field_type = inquirer.text(message="Enter the field type")
                    actor_to_edit.fields.append(ActorField(name=field_name, type=field_type))
                elif action == "Edit a field":
                    field_names = [field.name for field in actor_to_edit.fields]
                    field_name = inquirer.list_input(
                        message="Select the field to edit",
                        choices=field_names
                    )
                    for field in actor_to_edit.fields:
                        if field.name == field_name:
                            field.type = inquirer.text(message="Enter the new field type")
                elif action == "Delete a field":
                    field_names = [field.name for field in actor_to_edit.fields]
                    field_name = inquirer.list_input(
                        message="Select the field to delete",
                        choices=field_names
                    )
                    actor_to_edit.fields = [
                        field for field in actor_to_edit.fields
                        if field.name != field_name
                    ]
                elif action == "Exit":
                    break
        elif action == "Delete an Actor":
            names = list(actor_data.keys())
            name = inquirer.list_input(
                message="Select the Actor to delete",
                choices=names
            )
            del actor_data[name]
        elif action == "Exit":
            break

