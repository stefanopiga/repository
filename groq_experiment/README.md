# CrewAI Groq Experiment_newsletter for climber

## Overview

Questo repository ospita un'esercitazione con CrewAI, che mostra un'automazione avanzata basata sull'intelligenza artificiale attraverso compiti sequenzialie asincroni con callback e output predefiniti. È stato progettato per illustrare un flusso di lavoro migliorato per la creazione di strumenti di automazione di newsletter guidati dall'intelligenza artificiale.

## Features

- **Sequential Task Management:** Sfrutta la potenza dell'esecuzione sequenziale dei task per mantenere una base di codice pulita e scalabile.
- **Asynchronous Tasks:** Migliorare le prestazioni con operazioni non bloccanti, consentendo l'esecuzione simultanea dei task.
- **Callbacks:** Assicuratevi che ogni attività possa innescare azioni successive al completamento, consentendo un flusso di attività reattivo.
- **Expected Outputs:** Definire i risultati previsti per ogni attività, semplificando il debugging e garantendo il controllo della qualità.
- **Groq API:** Ho usaato API groq con modello llama3 70b; molto veloce e intelligente ma con alcune limitazioni consultabili qui:

https://console.groq.com/settings/limits

## Installation

Per iniziare con l'esperimento Groq_experiment, clonare il repository e installare le dipendenze necessarie.

```
git clone https://github.com/your-github-username/crewai-hierarchical-tutorial.git
cd groq_experiment
poetry lock
poetry install --no-root
poetry shell
```

## Usage

Per eseguire il bollettino di arrampicata CrewAI, eseguire lo script principale dopo aver impostato le variabili d'ambiente e la configurazione.

```
python main.py
```

## Structure

main.py: Lo script di ingresso che inizializza gli agenti e i compiti e forma l'equipaggio dell'IA.

agents.py: Definisce vari agenti come l'editor, il news fetcher, il news analyzer, il compilatore di newsletter e lo storyteller.

tasks.py: Contiene le definizioni dei compiti utilizzati dagli agenti per eseguire operazioni specifiche.

file_io.py: Gestisce le operazioni di input/output dei file, fondamentali per gestire il flusso asincrono dei dati.

Formazione dell'equipaggio:
L'equipaggio è composto da più agenti e compiti orchestrati per eseguire una complessa automazione della newsletter.

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
