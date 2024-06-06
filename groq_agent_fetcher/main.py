
"""MAIN section"""
import os
import time
import threading  # Aggiunto import per threading
from dotenv import load_dotenv
from crewai import Crew
from agents import ClimbingNewsletterAgents
from tasks import ClimbingNewsletterTasks


from file_io import save_markdown


def main():
    # officers' instances, duties and crew

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
