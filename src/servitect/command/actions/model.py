import questionary
from design_structure import DesignStructure, ModelField, Model


def actor(design_structure: DesignStructure) -> None:
    return edit_database(design_structure, True)


def model(design_structure: DesignStructure) -> None:
    return edit_database(design_structure, False)


def edit_database(design_structure: DesignStructure, is_actor=False) -> None:
    string_id = "Actor" if is_actor else "Model"

    if is_actor:
        data = design_structure.actor
    else:
        data = design_structure.model

    while True:
        action = questionary.select(
            f"Select an action for {string_id}",
            choices=[
                f"Create a new {string_id}",
                f"Edit an existing {string_id}",
                f"Delete an {string_id}",
                "Exit",
            ],
        ).ask()

        if action is None or action == "Exit":
            break

        if action == f"Create a new {string_id}":
            name = questionary.autocomplete(
                f"Enter the {string_id} name",
                choices=[
                    "default_actor_name",
                    "default_model_name",
                    "user",
                    "admin",
                    "customer",
                    "order",
                    "product",
                ],
            ).ask()

            if not name:
                continue

            fields = []

            while True:
                add_field = questionary.confirm("Would you like to add a field?").ask()
                if not add_field:
                    break

                field_name = questionary.autocomplete(
                    "Enter the field name",
                    choices=[
                        "id",
                        "username",
                        "first_name",
                        "last_name",
                        "email",
                        "password",
                        "date_of_birth",
                        "created_at",
                        "updated_at",
                    ],
                ).ask()

                field_type = questionary.autocomplete(
                    "Enter the field type",
                    choices=["int", "str", "date", "datetime", "float", "bool"],
                ).ask()

                if field_name and field_type:
                    fields.append(ModelField(name=field_name, type=field_type))

            permissions = {
                operation: questionary.checkbox(
                    f"Select permission level for {operation} operation",
                    choices=["self", "admin", "public"],
                    default="self",
                ).ask()
                for operation in ["create", "read", "update", "delete"]
            }

            new_actor = Model(fields=fields, permissions=permissions)
            data[name] = new_actor

        elif action == f"Edit an existing {string_id}":
            if not data:
                print(f"[bold red]No {string_id}s available to edit. [/bold red]")
                continue

            name = questionary.autocomplete(
                f"Select the {string_id} to edit",
                choices=list(data.keys()),
            ).ask()

            if not name:
                continue

            actor_to_edit = data[name]

            while True:
                sub_action = questionary.select(
                    f"Select an action for {string_id}: {name}",
                    choices=[
                        "Add a field",
                        "Edit a field",
                        "Delete a field",
                        "Edit permissions",
                        "Exit",
                    ],
                ).ask()

                if sub_action is None or sub_action == "Exit":
                    break

                if sub_action == "Add a field":
                    field_name = questionary.autocomplete(
                        "Enter the field name",
                        choices=[
                            "id",
                            "username",
                            "first_name",
                            "last_name",
                            "email",
                            "password",
                            "date_of_birth",
                            "created_at",
                            "updated_at",
                        ],
                    ).ask()

                    field_type = questionary.autocomplete(
                        "Enter the field type",
                        choices=["int", "str", "date", "datetime", "float", "bool"],
                    ).ask()

                    if field_name and field_type:
                        actor_to_edit.fields.append(
                            ModelField(name=field_name, type=field_type)
                        )

                elif sub_action == "Edit a field":
                    field_names = [field.name for field in actor_to_edit.fields]

                    field_name = questionary.autocomplete(
                        "Select the field to edit",
                        choices=field_names,
                    ).ask()

                    if field_name:
                        for field in actor_to_edit.fields:
                            if field.name == field_name:
                                new_type = questionary.autocomplete(
                                    "Enter the new field type",
                                    choices=[
                                        "int",
                                        "str",
                                        "date",
                                        "datetime",
                                        "float",
                                        "bool",
                                    ],
                                ).ask()
                                if new_type:
                                    field.type = new_type

                elif sub_action == "Delete a field":
                    field_names = [field.name for field in actor_to_edit.fields]

                    field_name = questionary.autocomplete(
                        "Select the field to delete",
                        choices=field_names,
                    ).ask()

                    if field_name:
                        actor_to_edit.fields = [
                            field
                            for field in actor_to_edit.fields
                            if field.name != field_name
                        ]

                elif sub_action == "Edit permissions":
                    for operation in ["create", "read", "update", "delete"]:
                        actor_to_edit.permissions[operation] = questionary.checkbox(
                            f"Select permission level for {operation} operation",
                            choices=["self", "admin", "public"],
                        ).ask()

        elif action == f"Delete an {string_id}":
            if not data:
                print(f"[bold red]No {string_id}s available to delete.[/bold red]")
                continue

            name = questionary.autocomplete(
                f"Select the {string_id} to delete",
                choices=list(data.keys()),
            ).ask()

            if name:
                del data[name]
