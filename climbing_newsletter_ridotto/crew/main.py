
"""newletter hierarchical system"""
from crewai import Crew, Process
from dotenv import load_dotenv
from config import llm_gpt4
from crew.agents import ClimbingNewsletterAgents
from crew.tasks import ClimbingNewsletterTasks
from file_io import save_markdown

load_dotenv()


class NewsLetterCrew():
    """news letter creator"""

 #   def __init__(self, climber_name):
 #       self.climber_name = climber_name
#
 #   def run(self):
 #       """run's definition"""

    # Initialize the agents and tasks
    agents = ClimbingNewsletterAgents()
    tasks = ClimbingNewsletterTasks()

    climber_name = "Patrick Edlinger"


    # Instantiate the agents
    editor = agents.editor_agent()
    news_fetcher = agents.news_fetcher_agent()
    news_analyzer = agents.news_analyzer_agent()
    newsletter_compiler = agents.newsletter_compiler_agent()
    storyteller = agents.storyteller_agent()
    # Instantiate the tasks
    fetch_news_task = tasks.fetch_news_task(news_fetcher)
    analyze_news_task = tasks.analyze_news_task(
        news_analyzer, [fetch_news_task])
    compile_newsletter_task = tasks.compile_newsletter_task(
        newsletter_compiler, [analyze_news_task])
    write_story_task = tasks.write_story_task(
        storyteller, [compile_newsletter_task],
        save_markdown)
     # Form the crew
    crew = Crew(
        agents=[editor, news_fetcher, news_analyzer, newsletter_compiler, storyteller],
        tasks=[fetch_news_task, analyze_news_task, compile_newsletter_task, write_story_task],
        process=Process.hierarchical,
        manager_llm=llm_gpt4,
        verbose=2
    )
     # Kick off the crew's work
    results = crew.kickoff()

    print("Crew usage", crew.usage_metrics)

    print('-------------------------------')
    print('-------------------------------')
    print("Crew work results:")
    print('-------------------------------')
    print('-------------------------------')
    print(results)

