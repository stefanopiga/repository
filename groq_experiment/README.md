# CrewAI Hierarchical Tutorial

## Overview

Questo repository ospita un'esercitazione con CrewAI, che mostra un'automazione avanzata basata sull'intelligenza artificiale attraverso compiti sequenzialie asincroni con callback e output predefiniti. È stato progettato per illustrare un flusso di lavoro migliorato per la creazione di strumenti di automazione di newsletter guidati dall'intelligenza artificiale.

## Features

- **Sequential Task Management:** Sfrutta la potenza dell'esecuzione sequenziale dei task per mantenere una base di codice pulita e scalabile.
- **Asynchronous Tasks:** Improve performance with non-blocking operations, allowing tasks to run concurrently.
- **Callbacks:** Ensure that each task can trigger subsequent actions upon completion, enabling a reactive task flow.
- **Expected Outputs:** Define the anticipated results for each task, streamlining debugging and ensuring quality control.
- **Groq API:** ho usaato API groq con modello llama3 70b; molto veloce e intelligente ma con alcune limitazioni consultabili qui:

## Installation

To get started with the Groq_experiment, clone the repository and install the necessary dependencies.

```
git clone https://github.com/your-github-username/crewai-hierarchical-tutorial.git
cd groq_experiment
poetry lock
poetry install --no-root
poetry shell
```

## Usage

To run the CrewAI climbing newsletter, execute the main script after setting up your environment variables and configuration.

```
python main.py
```

## Structure

main.py: The entry point script that initializes the agents and tasks, and forms the AI crew.

agents.py: Defines various agents like the editor, news fetcher, news analyzer, and newsletter compiler.

tasks.py: Contains the task definitions that are used by the agents to perform specific operations.

file_io.py: Manages file input/output operations, crucial for handling the async flow of data.

Crew Formation
The crew is composed of multiple agents and tasks orchestrated to perform complex newsletter automation.

```
crew = Crew(
    agents=[editor, news_fetcher, news_analyzer, newsletter_compiler, storyteller],
    tasks=[fetch_news_task, analyze_news_task, compile_newsletter_task ,write_story_task],
    process=Process.sequential,
    verbose=2
)
```

## Particolari

ci sono alcuni problemi con la scrittura delle 2000 parole da parte dello storyteller, probabilmente per via di informazioni non abbastanza accurate dai task precedenti; devo lavorare sull'abbondanza di dettagli.
