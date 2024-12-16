# Documentation of Sources and Decisions

## Introduction
This document outlines the sources of information and the rationale behind key decisions made during the development of the CLI tool for interacting with the Artifactory API. The tool was implemented using the Python libraries `click`, `requests`, `os`, and `json`.

---

## Sources Used

### 1. Official Documentation
- **Artifactory REST API Documentation**  
  The Artifactory API documentation was the primary source for understanding the available endpoints, required headers, authentication mechanisms, and response structures.  
  **Key Link**: [Artifactory REST API](https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API)

- **Click Documentation**  
  The official `click` documentation was consulted to understand how to build command-line interfaces effectively. It provided details on decorators, options, arguments, and command structures.  
  **Key Link**: [Click Documentation](https://click.palletsprojects.com/)

- **Requests Library Documentation**  
  The Python `requests` library documentation was used to implement HTTP calls for interacting with the Artifactory API. It provided guidance on making GET, POST, PUT, and DELETE requests and handling response statuses.  
  **Key Link**: [Requests Documentation](https://docs.python-requests.org/)

### 2. Community Resources
- **Stack Overflow**: Referenced for troubleshooting issues, such as handling authentication tokens and best practices for error handling in CLI tools.
- **GitHub Repositories**: Explored for examples of integrating Artifactory APIs and managing environment variables.

---

## Decisions Made

### 1. Technology Stack
- **`click`**: Chosen for its simplicity and flexibility in creating CLI applications. Its intuitive syntax allows for rapid development of user-friendly command-line tools.
- **`requests`**: Selected for making HTTP requests due to its ease of use and robustness in handling various HTTP methods.
- **`os` and `json`**: Utilized for managing environment variables (e.g., API keys, base URLs) and processing API responses in JSON format.

### 2. Authentication
- Implemented token-based authentication as it is more secure and widely supported by Artifactory.
- Environment variables (e.g., `ARTIFACTORY_API_TOKEN` and `ARTIFACTORY_URL`) were used to store sensitive information, avoiding hardcoding them in the script.

### 3. Error Handling
- Centralized error handling was implemented using Python exceptions to catch common issues such as:
  - Invalid or missing API tokens.
  - Network-related errors (e.g., timeouts).
  - Unexpected API responses (e.g., HTTP 404 or 500 errors).
- User-friendly error messages were displayed for all common issues to improve the CLI's usability.

### 4. Command Structure
- Commands were grouped logically to reflect common Artifactory tasks:
  - `upload`: For uploading artifacts.
  - `download`: For downloading artifacts.
  - `delete`: For removing artifacts.
  - `list`: For listing artifacts in a repository.
- These commands were implemented as separate `click` commands for modularity and ease of maintenance.

### 5. API Integration
- Each command interacts directly with the Artifactory API endpoints. The `requests` library was used to send requests and handle responses. Any non-2xx response codes were logged, and appropriate error messages were displayed to the user.

### 6. Output Formatting
- JSON responses from the Artifactory API were parsed using the `json` library for a structured and readable output. An optional flag (`--raw`) was provided for users to view raw API responses.

### 7. Environment Variable Management
- The `os` module was used to retrieve environment variables for storing sensitive data (e.g., API tokens). Instructions for setting up a `.env` file were included in the documentation for user convenience.

---

## Challenges and Solutions

### Authentication Issues
- Early issues with token-based authentication were resolved by testing with a personal token and verifying request headers via the API documentation.

### Error Handling
- Extensive testing with mock API calls helped anticipate and handle edge cases.

### User Experience
- Feedback from peers was incorporated to improve the command structure and make error messages more descriptive.

---

## Conclusion
The project leveraged widely adopted Python libraries and adhered to best practices in CLI development. Key decisions were guided by documentation, real-world use cases, and feedback from users. This modular and extensible approach ensures maintainability and scalability for future enhancements.

---
