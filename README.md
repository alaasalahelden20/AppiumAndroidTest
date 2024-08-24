#     AppiumAndroidTest

## Overview

This is a Django application for managing and testing mobile apps. It provides functionalities to upload, view, edit, and delete apps, as well as perform automated tests using Appium.

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Docker Configuration](#docker-configuration)

- [Usage](#usage)

## Requirements

- Python 3.x
- Django 4.x
- MySQL or SQLite
- Appium
- Selenium

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/alaasalahelden20/AppiumAndroidTest.git]
    cd AppiumAndroidTest.git
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Installation

## Installation

1. **Install MySQL Server:**

    - Ensure MySQL Server is installed and running on your machine or accessible through a network.
    - Create a database for your project.

2. **Install MySQL Python library:**

    You need `mysqlclient` to connect Django to MySQL. Install it using:

    ```bash
    pip install mysqlclient
    ```

3. **Configure the database settings:**

    Edit the `settings.py` file in your Django project and update the `DATABASES` section with your MySQL configuration.

    Example configuration for MySQL:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',  # Or your MySQL server instance #db in case using docker
            'PORT': '3306',       # Default MySQL port
        }
    }
    ```

    }
    ```

    Example for SQLite:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

## Running the Application

1. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

3. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

## Configuration

1. **Environment Variables:**

    - Ensure to set up the environment variables required for your project, such as `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, etc. You can use a `.env` file and the `django-environ` package to manage these.

    Example `.env` file:

    ```
    DJANGO_SECRET_KEY=your-secret-key
    DJANGO_DEBUG=True
    ```

2. **Appium Setup:**

    - Ensure you have Appium installed and configured. You may need to install the Appium server and set up the required drivers for your tests.
## Docker Configuration

If you prefer to use Docker for setting up your application, follow these steps:

1. **Ensure Docker and Docker Compose are installed:**

    - [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. **Build and start the Docker containers:**

    Navigate to your project directory (where your Dockerfile and `docker-compose.yml` are located) and run:

    ```bash
    docker-compose up --build
    ```

    This command builds the Docker images and starts the containers for both the Django application and MySQL database. The application will be accessible at `http://127.0.0.1:8000/`.

3. **Apply database migrations inside the Docker container:**

    ```bash
    docker-compose run web python manage.py migrate
    ```

4. **Create a superuser inside the Docker container:**

    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

## Usage

1. **Access the Admin Interface:**

    - Navigate to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials to manage the application data.

2. **Upload a New App:**

    - Use the "Upload a new App" link on the main page to add new applications.

3. **Test Your Application:**

    - Follow the instructions in the `apps_manager/views.py` file to run Appium tests on your uploaded apps.


