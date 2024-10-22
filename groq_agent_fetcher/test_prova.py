"""test telemetria"""
import json
import os
import requests
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool


class CustomTelemetryTool(BaseTool):
    """strumento telemetria"""

    name: str = "CustomTelemetryTool"
    description: str = "Strumento per la telemetria personalizzata."

    def _run(self, data: dict) -> str:
        # Implementa la logica per inviare i dati di telemetria a un endpoint remoto
        try:
            url = "http://telemetry.crewai.com:4318/v1/traces"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(
                url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return "Telemetria inviata con successo"
        except requests.exceptions.RequestException as e:
            return f"Errore durante l'invio della telemetria: {e}"


# Utilizzo del nuovo strumento di telemetria
telemetry_tool = CustomTelemetryTool()

# Creazione degli agenti con telemetria abilitata
researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    verbose=True,
    memory=True,
    backstory="Driven by curiosity, you're at the forefront of innovation.",
    tools=[telemetry_tool],
    allow_delegation=True
)

writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    verbose=True,
    memory=True,
    backstory="With a flair for simplifying complex topics, you craft engaging narratives.",
    tools=[telemetry_tool],
    allow_delegation=False
)

# Creazione dei compiti
research_task = Task(
    description="Identify the next big trend in {topic}.",
    expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
    tools=[telemetry_tool],
    agent=researcher
)
test_prova.py

write_task = Task(
    description="Compose an insightful article on {topic}.",
    expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
    tools=[telemetry_tool],
    agent=writer,
    async_execution=False,
    output_file='new-blog-post.md'
)

# Formazione del crew con telemetria
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

# Avvio del crew
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)
