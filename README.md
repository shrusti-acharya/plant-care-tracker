# Houseplant Watering & Care Tracker

A dynamic web application built with Flask and delivered via an automated CI/CD pipeline.

## Features
- Dynamic houseplant registration and automatic watering schedule calculation
- REST API endpoint (\/api/plants\) returning JSON records
- Health check route (\/health\) displaying status and running Git commit ID
- Containerized using Docker for parity across environments

## CI/CD Pipeline
- **Continuous Integration**: Triggers on push/PR to \main\. Runs Flake8 linter and Pytest test suite.
- **Build**: Builds Docker container and executes a smoke test verifying the \/health\ route.
- **Continuous Deployment**: Triggers a webhook deployment to Render upon successful merge/push to \main\.
## Architecture Flowgit add README.md
