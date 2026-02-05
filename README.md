# Autonomous Code Reviewer & Security Auditor
An agentic RAG-based system that aims to assist developers in identifying bugs, security vulnerabilities (with explanation), risk assessment, and code quality issues.


## Overview
The aim of this project is to build an autonomous code review and security auditing system that analyses source code using Large Language Models (LLMs) along with Retrieval-Augmented Generation (RAG).
The system performs static analysis on code, identifies potential security vulnerabilities, any bad coding practices used, and performance issues, and provides human-readable explanations and remedies to make the code better.
It examines source files, understands code structure, and maps risky patterns against a knowledge base of known vulnerabilities, bad practices, and performance issues. The system then explains why a particular line is problematic and suggests possible improvement strategies.

## Motivation
Manual code reviews are time-consuming, full of errors, and just not efficient. Existing automated tools lack explainability or are limited to rule-based checks.
This project works on agentic LLM-based systems, combined with a structured knowledge base of known issues. It aims to assist developers by:
-   Automatically identifying risky code patterns.
-   Explaining why a piece of code is problematic.
-   Suggesting improvements in a contextual manner.

## Objectives
-   <h3>Automated Code Analysis</h3>
    To design a system that is able  to perform static analysis on source code and automatically detect security vulnerabilities, bad coding practices, and performance inefficiencies.
-   <h3>Agentic RAG-based reasoning</h3>
    To implement an Agentic RAG architecture where multiple specialised agents (security, performance, and best-practice agents) analyze code chunks independently, guide by classifier agent.
-   <h3>Explainability and Developer Understanding</h3>
    To ensure issues are flagged as well as explained such that the developer can understand the root cause and potential impact of each issue.
-   <h3>Safe and Isolated Execution Environment</h3>
    To use Docker-based containerization to analyze user-provided code in a secure and isolated environment, ensuring that the host system is protected from malicious or unstable inputs.
-   <h3>Risk Visualization and Insight Generation</h3>
    To provide visual representation such as code heatmaps and dependency graphs that highlight high risk areas of a codebase.

## Impact and Significance of the Project
From a software engineering perspective, it addresses the issue of complex codebases, where manual reviews are often inefficient and time consuming. By automating a large part of this process, the tool can help the developer identify issues earlier, and improve overall code quality.
From a security point of view, the system assists in detecting common vulnerabilities, hence reducing the risk of security breaches in production systems.
It demonstrates how LLMs can be used not just for code generation, but for reasoned analysis and decision-making, supported by knowledge bases.

## Team
This project is being developed collaboratively by a team, with different responsibilities:
-   Agentic RAG and analysis logic
-   Containerization using Docker
-   Data visualization and reporting


