1. Core Computing Concepts

Computer Terminal / Shell / Bash
A text interface for giving commands to your computer. Example: typing ls to list files.

Command Line
The line where you type a shell command.

Path
The location of a file or folder in your computer. Example: 02_Projects/04_AvatarAssistant/README.md.

Environment Variable
A temporary setting that stores a value (like an API key) available to your programs.

Script
A text file that contains a sequence of commands for the computer to run automatically.

⸻

2. Version Control (Git + GitHub)

Git
A system that tracks changes to files over time, like a time machine for code.

Repository (Repo)
A folder that Git manages. It contains your code, docs, and history.

Commit
A snapshot of your project at a specific moment. You write a short message describing what changed.

Push
Send commits from your computer to GitHub (the cloud copy).

Pull
Download new commits from GitHub to your computer.

Branch
A separate timeline of changes used for experimenting safely.

Merge
Combine changes from one branch into another.

.gitignore
A file listing items Git should not track (e.g., large files, venv folders).

GitHub
A website that hosts Git repositories, letting you share and collaborate.

⸻

3. Python Project Structure

Python
A programming language used for AI, data, and automation.

Virtual Environment (venv)
A self-contained sandbox that holds the exact Python packages for one project.

Requirements.txt
A list of all Python packages the project needs to run.

Dependency
A library or external module that your project relies on (e.g., requests, pydantic).

Package / Module
Reusable pieces of Python code. A folder with an __init__.py file is a package.

Import
The command Python uses to load another module.

Script Entry Point
The file that runs first when you start a program (e.g., cli.py).

⸻

4. Automation & Testing

CI/CD (Continuous Integration / Continuous Deployment)
Automated workflows that run tests, build your code, and deploy it whenever you push to GitHub.

Test (Unit Test)
A small check to verify one part of your program works correctly.

Pytest
A popular Python tool for running tests automatically.

Pre-commit Hook
A script that checks or formats your code before each commit.

⸻

5. Agentic AI System Concepts

Agent
A system that perceives, reasons, and acts toward a goal using AI tools.

LLM (Large Language Model)
An AI model trained to understand and generate human-like text (e.g., GPT).

Prompt
Text input given to an LLM to guide its response.

Tool / Plugin / Action
External capability an agent can call (like searching the web or summarizing text).

Autonomy Loop
The feedback cycle of observe → reason → act → evaluate.

Memory
An agent’s record of past inputs, decisions, or results to inform future actions.

Reflection
When an agent reviews its own performance and adjusts behavior.

Workflow / Pipeline
A sequence of connected steps that transform input to output (e.g., record → transcribe → summarize).

⸻

6. Data and File Terms

Dataset
A structured collection of data used for analysis or model training.

Data Folder
Where input/output files are stored (e.g., data/runs/).

Manifest File
A record describing what was processed, when, and how.

Config File
Stores adjustable settings so you can change behavior without editing code.

⸻

7. Project Management Terms

README.md
Main document explaining what the project does and how to run it.

CHANGELOG.md
Chronological record of notable changes to the project.

Milestone
A dated checkpoint in the project timeline (e.g., “M1: architecture running by Nov 20”).

Task File (tasks.md)
List of concrete next steps to reach the next milestone.

Metrics.md
Where you record how you’ll measure success and system performance.
