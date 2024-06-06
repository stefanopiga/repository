
"""Creazione file output"""
from datetime import datetime
import os


def save_markdown(task_output):
    """Method for saving results to a Markdown file."""
    try:
        # Prepara il nome del file e il percorso
        today_date = datetime.now().strftime('%Y-%m-%d')
        base_path = r"C:/Users/user/Desktop/repository/groq_agent_fetcher/risultato/01"
        filename = f"{today_date}.md"
        full_path = os.path.join(base_path, filename)

        # Prepara il contenuto del file
        output_string = task_output.result() if hasattr(
            task_output, 'result') and callable(task_output.result) else str(task_output)

        # Scrive il contenuto nel file Markdown
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(output_string)
        print(f"Newsletter saved as {full_path}")

    except ImportError as e:  # Cattura eccezioni più generiche legate a errori di I/O
        print(f"Failed to save the newsletter: {e}")
