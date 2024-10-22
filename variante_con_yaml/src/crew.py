

#definizione della CREW
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from agentops.agent import track_agent
import agentops
from src.tools.custom_tool import SearchTools


from file_io import save_markdown


agentops.init()

@CrewBase
class ClimbingNewsLetterCrew:
    """ClimbingNewsLetterCrew crew for write a newsletter on climbing theme"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    def __init__(self) -> None:
          # Groq
          self.groq_llm = ChatGroq(
              temperature=0,
              groq_api_key=os.environ.get("GROQ_API_KEY"),
              model_name="llama3-70b-8192",
          )


    @track_agent(name="news_fetcher")
    @agent
    def news_fetcher(self) -> Agent:
        """Agent restponsable for fetching news about name_climber."""

        return Agent(
            config=self.agents_config["news_fetcher"],
            tools=[SearchTools.search_internet],
            allow_delegation=True,
            memory=True,
            llm=self.groq_llm,
            verbose=True,
            max_iter=2
        )


    @track_agent(name="news_analyzer")
    @agent
    def news_analyzer(self) -> Agent:
        """Agent responsible for analyzing fetching output."""

        return Agent(
            config=self.agents_config["news_analyzer"],
            tools=[SearchTools.search_internet],
            allow_delegation=True,
            memory=True,
            llm=self.groq_llm,
            verbose=True,
            max_iter=2
        )


    @track_agent(name="newsletter_compiler")
    @agent
    def newsletter_compiler(self) -> Agent:
        """Agent responsible for analyzing fetching output."""

        return Agent(
            config=self.agents_config["newsletter_compiler"],
            tools=[SearchTools.search_internet],
            allow_delegation=True,
            memory=True,
            llm=self.groq_llm,
            verbose=True,
            max_iter=2
        )


    @track_agent(name="storyteller")
    @agent
    def storyteller(self) -> Agent:
        """Agent responsible for analyzing fetching output."""

        return Agent(
            config=self.agents_config["storyteller"],
            tools=[SearchTools.search_internet],
            allow_delegation=True,
            memory=True,
            llm=self.groq_llm,
            verbose=True,
            max_iter=2
        )


    @task
    def fetch_news_task(self) -> Task:
        """Task to fetch climbing news from internet tool."""
        return Task(
            config=self.tasks_config["fetch_news_task"],
            agent=self.news_fetcher(),
            output_file="fetched_news.md",
        )

    @task
    def analyze_news_task(self, context) -> Task:
        """Task to analyze comments and generate insights."""
        return Task(
            config=self.tasks_config["analyze_news_task"],
            agent=self.news_analyzer(),
            context=context,
            human_input=True,
            output_file="analyzed_news.md",
        )


    @task
    def newsletter_compiler_task(self, context) -> Task:
        """Task to analyze comments and generate insights."""
        return Task(
            config=self.tasks_config["newsletter_compiler_task"],
            agent=self.newsletter_compiler(),
            human_input=True,
            context=context,
            output_file="newsletter_compiled.md",
        )


    @task
    def write_story_task(self, context, callback_function) -> Task:
        """Task to analyze comments and generate insights."""
        return Task(
            config=self.tasks_config["write_story_task"],
            agent=self.storyteller(),
            context=context,
            callbacks=callback_function,
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the climbing newsletter crew"""

        news_fetcher = self.news_fetcher()
        news_analyzer = self.news_analyzer()
        newsletter_compiler = self.newsletter_compiler()
        storyteller = self.storyteller()

        fetch_news_task = self.fetch_news_task()
        analyze_news_task = self.analyze_news_task([fetch_news_task])
        newsletter_compiler_task = self.newsletter_compiler_task([analyze_news_task])
        write_story_task = self.write_story_task([newsletter_compiler_task], save_markdown)

        return Crew(
            agents=[
                news_fetcher,
                news_analyzer,
                newsletter_compiler,
                storyteller,
            ],
            tasks=[
                fetch_news_task,
                analyze_news_task,
                newsletter_compiler_task,
                write_story_task,
            ],
            process=Process.sequential,
            memory=False,
            max_rpm=2,
            verbose=2,
        )
