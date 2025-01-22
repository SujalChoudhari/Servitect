# Servitect - Python Microservice Design Tool (⚠️WIP)

Servitect is a command-line tool designed to help you quickly design and structure microservices. Inspired by the original Servitect project ([https://github.com/kushkapadia/servitect](https://github.com/kushkapadia/servitect)), this Python version aims to provide a similar streamlined experience for defining the core aspects of your services, such as user roles, data models, scheduled tasks, and AI integrations, all from a single configuration file.

## Features

*   **Declarative Design:** Define your service's architecture using a structured configuration file.
*   **Interactive CLI:** A user-friendly command-line interface guides you through the design process.
*   **Configurable Service Elements:**
    *   Define project name, version, and port settings.
    *   Configure database connection details.
    *   Manage security with JWT secret keys.
    *   Create and manage user roles with custom fields and access permissions.
    *   Define data structures for your application.
    *   Schedule periodic tasks for your service.
    *   Integrate AI capabilities with API keys and assistant configurations.
    *   Activate or deactivate testing mode.
*   **Visual Design Overview:** View your entire service design in a structured, easy-to-understand dashboard within your terminal.
*   **Configuration File Driven:** All design configuration is stored in a `servitect.schema.json` file.

## Configuration File

The entire design of your service is stored within a `servitect.schema.json` file. This allows you to easily track and modify the structure of your microservice project.

## Credits

*   Inspired by the original Servitect project: [https://github.com/kushkapadia/servitect](https://github.com/kushkapadia/servitect).