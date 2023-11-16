# Education Testing Platform

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The **Education Testing Platform** is a web application built with Django, designed to manage educational materials and
conduct tests related to the content. This platform allows educators to create tests, associate them with specific
educational materials, and enable students to take those tests.

## Features

- **User Authentication:** Users can register, log in, and manage their profiles. Only authenticated users can create,
  edit, and run tests.

- **Test Management:** Educators can create, update, and delete tests. Tests can be associated with specific educational
  materials.

- **Question and Answer Management:** For each test, educators can create a set of questions with associated answers.
  Answers can be marked as correct.

- **Test Execution:** Students can take tests by answering questions. The platform checks the answers' correctness and
  records test results.

- **Publication Control:** Educators can control the publication status of tests, educational materials, and publication
  requests.

## Project Structure

The project is structured into several Django apps, each responsible for specific functionality:

- **education_content:** Manages educational materials, such as chapters and materials with associated content.

- **users:** Handles user authentication, registration, and user profiles.

- **tests:** Manages tests, questions, and answers. It provides features for creating and running tests.

The project uses Django's built-in authentication system for user management.

## Installation

Follow these steps to set up the Education Testing Platform on your local development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/Khasanov1988/Self-learning_platform.git
   ```
2. Navigate to the project directory:
    ```bash
    cd education-testing-platform
    ```
3. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:

   Windows:
    ```bash
    venv\Scripts\activate
    ```
   Linux/macOS:
    ```bash
    source venv/bin/activate
    ```
5. Install project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Fill .env file (use .env.example):
    ```bash
    nano .env
    ```
7. Perform initial database migrations:
    ```bash
    python manage.py migrate
    ```
8. Collect static:
    ```bash
    python manage.py collectstatic
    ```
9. Create a superuser (admin) account for managing the platform:
    ```bash
    python manage.py csu
    ```
10. Fill necessary tables in database
    ```bash
    python manage.py renew_data_bases
    ```
11. Start the development server:
    ```bash
    python manage.py runserver
    ```

The project will be accessible at http://127.0.0.1:8000/.

## Usage

Log in with your superuser account to access the admin panel.

Create educational materials, chapters, and materials.

Create tests and associate them with specific materials.

Add questions and answers to your tests, marking correct answers.

Log in as a regular user and take tests.

Check test results and manage publication status from the admin panel.

## Contributing

Contributions to this project are welcome. If you have ideas for improvements or new features, please submit issues or
pull requests. Make sure to follow the project's coding standards and guidelines.

## License

This project is licensed under the MIT License