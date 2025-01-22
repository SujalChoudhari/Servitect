import inquirer
from design_structure import DesignStructure
from rich import print

def validate_jwt_secret(secret: str) -> bool:
    return len(secret) >= 8  # Example: JWT secret should be at least 8 characters long

def security(design_structure: DesignStructure) -> None:
    security_data = design_structure.security

    while True:
        questions = [
            inquirer.Text(
                "jwt_secret",
                message="Enter JWT Secret",
                default=security_data.jwt_secret,
            ),
        ]

        answers = inquirer.prompt(questions)
        jwt_secret = answers["jwt_secret"]

        if validate_jwt_secret(jwt_secret):
            security_data.jwt_secret = jwt_secret
            break
        print("[bold red]Invalid JWT secret. It must be at least 8 characters long.[/bold red]")