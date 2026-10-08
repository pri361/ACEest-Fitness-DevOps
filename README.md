# ACEest Fitness & Gym

A small Flask application for managing gym members and workout records. This project was built as part of the DevOps assignment to practice Git/GitHub, Pytest, Docker, Jenkins and GitHub Actions.

## Features

- Add and view gym members
- Add and view workout records
- Basic form validation
- Health check endpoint
- Simple responsive web interface
- Automated tests using Pytest
- Docker support
- Jenkins build and test
- GitHub Actions CI pipeline

## Technologies Used

- Python 3.13
- Flask
- Pytest
- Git and GitHub
- Docker
- Jenkins
- GitHub Actions

## Project Structure

```text
ACEest-Fitness-DevOps/
├── .github/
│   └── workflows/
│       └── main.yaml
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── members.html
│   ├── add_member.html
│   ├── workouts.html
│   └── add_workout.html
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .gitignore
```

## Run the application locally

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps
```

Create and activate a virtual environment.

### Windows

```powershell
python -m venv .venv
.venv\Scriptsctivate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

The application runs on port 5000.

Open:

```text
http://localhost:5000
```

## Running the tests

The project uses Pytest for unit testing.

Run:

```bash
python -m pytest -v
```

The current test suite contains 11 tests covering the main pages, health endpoint, member registration and validation, and workout registration and validation.

## Running with Docker

Build the Docker image:

```bash
docker build -t aceest-fitness .
```

Run the container:

```bash
docker run -d --name aceest-fitness-app -p 5000:5000 aceest-fitness
```

The application can then be accessed at:

```text
http://localhost:5000
```

Check the running container:

```bash
docker ps
```

Stop it with:

```bash
docker stop aceest-fitness-app
```

## Jenkins

Jenkins is used as an additional build and validation step.

The Jenkins job:

1. Checks out the latest code from the `main` branch.
2. Builds the Docker image.
3. Runs the Pytest test suite inside the Docker container.
4. Marks the build as successful only when the steps pass.

The Jenkins build script is:

```bash
#!/bin/bash

set -e

echo "=== Building Docker image ==="
docker build -t aceest-fitness:jenkins .

echo "=== Running Pytest inside Docker ==="
docker run --rm aceest-fitness:jenkins python -m pytest -v

echo "=== JENKINS BUILD AND QUALITY GATE PASSED ==="
```

## GitHub Actions

GitHub Actions is configured in:

```text
.github/workflows/main.yaml
```

The workflow runs automatically on pushes and pull requests.

It has three stages:

1. **Build and Lint**
   - Checks out the code
   - Sets up Python
   - Installs dependencies
   - Checks Python syntax

2. **Docker Image Assembly**
   - Builds the Docker image

3. **Automated Testing**
   - Builds the Docker image for testing
   - Runs the Pytest suite inside the container

If a test or build fails, the GitHub Actions workflow fails.

## Health Check

The application provides a health endpoint:

```text
/health
```

Example:

```text
http://localhost:5000/health
```

It returns the application's health status in JSON format.

## Development

Git is used for version control. Changes are committed with short messages describing the work, for example:

```text
feat: initialize ACEest Flask application
feat: add member and workout management
test: add pytest coverage and Docker containerization
ci: add GitHub Actions pipeline
```

The `main` branch contains the working version of the project.
