
"""MAIN section"""
import os
import time
from dotenv import load_dotenv
from crewai import Crew
from agents import ClimbingNewsletterAgents
from tasks import ClimbingNewsletterTasks

from file_io import save_markdown

def main():
    """officers' instances, duties and crew"""
    load_dotenv()  # Load environment variables

    # Initialize tasks with agents and specific climber names
    climber_name = "Patrick Edlinger"

    # Initialize agents
    agents = ClimbingNewsletterAgents(climber_name)
    tasks = ClimbingNewsletterTasks()

    # Initialize agents, handling potential None returns if token limit exceeded
    editor = agents.editor_agent()
    news_fetcher = agents.news_fetcher_agent()
    news_analyzer = agents.news_analyzer_agent()
    newsletter_compiler = agents.newsletter_compiler_agent()
    storyteller = agents.storyteller_agent()

#   if not all([editor, news_fetcher, news_analyzer, newsletter_compiler, storyteller]):
#       logging.error("Could not initialize all agents due to token limit issues.")
#       return  # Exit if not all agents could be created


    fetch_news_task = tasks.fetch_news_task(news_fetcher)
    analyze_news_task = tasks.analyze_news_task(news_analyzer, [fetch_news_task])
    compile_newsletter_task = tasks.compile_newsletter_task(newsletter_compiler, [analyze_news_task])
    write_story_task = tasks.write_story_task(storyteller, [compile_newsletter_task], save_markdown)

    # Form the crew
    crew = Crew(
        agents=[editor, news_fetcher, news_analyzer,
            newsletter_compiler, storyteller],
        tasks=[fetch_news_task, analyze_news_task, compile_newsletter_task, write_story_task],
       # process=Process.hierarchical,
       # manager_llm= manager_llm,
        verbose=True,
        max_rpm=29
    )

    # Kick off the crew
    start_time = time.time()

    # Execute the crew
    results = crew.kickoff()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Crew kickoff took {elapsed_time} seconds.")
    print("Crew usage", crew.usage_metrics)


if __name__ == "__main__":
    main()
