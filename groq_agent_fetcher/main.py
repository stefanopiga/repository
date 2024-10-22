
"""MAIN section"""
import os
import time
import threading
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace

# Aggiunto import per threading
from dotenv import load_dotenv
from crewai import Crew
from agents import ClimbingNewsletterAgents
from tasks import ClimbingNewsletterTasks


from file_io import save_markdown


def configure_otlp_exporter():
    # Configura la strategia di retry
    retry_strategy = Retry(
        total=3,  # Numero totale di tentativi
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS",
                         "POST"],  # Metodi da ritentare
        backoff_factor=1  # Attesa 1s, 2s, 4s, ecc. tra i tentativi
    )

    # Configura l'adattatore HTTP con il retry
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)

    # Crea l'exporter OTLP con la sessione configurata e un timeout maggiore
    span_exporter = OTLPSpanExporter(
        endpoint="http://telemetry.crewai.com:4318/v1/traces",
        session=http,
        timeout=30  # Aumenta il timeout a 30 secondi
    )

    # Configura il TracerProvider e aggiungi il BatchSpanProcessor
    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Imposta il TracerProvider configurato come predefinito
    trace.set_tracer_provider(tracer_provider)


def main():
    # officers' instances, duties and crew

    # Configura l'exporter OTLP
    configure_otlp_exporter()

    load_dotenv()  # Load environment variables

    # Initialize tasks with agents and specific climber names
    climber_name = "Patrick Edlinger"

    # Initialize agents
    agents = ClimbingNewsletterAgents(climber_name)
    tasks = ClimbingNewsletterTasks()

    # Initialize agents, handling potential None returns if token limit exceeded
    news_fetcher = agents.news_fetcher_agent()
    # news_analyzer = agents.news_analyzer_agent()

    # initialize tasks
    fetch_news_task = tasks.fetch_news_task(news_fetcher, save_markdown)
    # analyze_news_task = tasks.analyze_news_task(
    #   news_analyzer, [fetch_news_task], save_markdown)

    # Form the crew
    crew = Crew(
        # agents=[news_fetcher, news_analyzer],
        # tasks=[fetch_news_task, analyze_news_task],
        agents=[news_fetcher],
        tasks=[fetch_news_task],
        verbose=True,
        max_rpm=29
    )

    # Kick off the crew
    start_time = time.time()

    # Execute the crew
    results = crew.kickoff()

    # Assicurarsi che tutti i thread siano completati
    for thread in threading.enumerate():
        if thread is not threading.current_thread():
            thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Crew kickoff took {elapsed_time} seconds.")
    print("Crew usage", crew.usage_metrics)
    print(results)


if __name__ == "__main__":
    main()
