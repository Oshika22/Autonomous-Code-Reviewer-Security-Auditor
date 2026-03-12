# Dockerized Execution Environment

## Overview
To make sure that the system runs across different development environments, the Autonomous Code Reviewer & Security Auditor is being containerised using Docker. This enables the project to operate in a controlled and isolated environment where dependencies, runtime configurations, and system behaviour remain reproducible regardless of the host operating system.
The aim is to make a Docker-based multi-container architecture that separates the backend (code analysis part), vertor database service, data visualisation and frontend interface.

## Architecture
Container is orchestrated using Docker Compose.

Host OS
    - Docker Engine
        - Backend Container
        - Vector Database Container
        - Frontend Container

All containers communicate through a private Docker bridge network, ensuring controlled service interaction without exposing internal components unnecessarily to the host system.

## Backend Container

The backend container executes the static analysis workflow by processing the provided source code, invoking the agentic RAG pipeline.

## Vector Database Service

## Frontend Container

A Nginx-based frontend container used as a placeholder interface for the system. It will host user interface and visualise analysis results.