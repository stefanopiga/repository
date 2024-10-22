
"""definizione assistente AI"""
import os
from textwrap import dedent
from crewai import Agent
from langchain_groq import ChatGroq
# from langchain.agents import load_tools
from tools.search_tools import SearchTools


# Human Tools
# human_tools = load_tools(["human"])


class ClimbingNewsletterAgents():
    """Team of agents hired to create a newsletter."""

    def __init__(self, climber_name):
        # Istanze LLM

       #     llama3_8b = "llama3-8b-8192"
       #     llama3_70b = "llama3-70b-8192"

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        self.climber_name = climber_name  # Store the climber's name

    def news_fetcher_agent(self):
        """Agent to analyze the acquired information."""

        return Agent(
            role='News Fetcher',
            goal=dedent(f"""\
                Research and fetch detailed stories and biographical
                elements of iconic climber: {self.climber_name}"""),
            backstory=dedent("""\
                As a dedicated researcher of climbing history you delve into
                archives and current records to bring the most compelling and detailed stories
                to light."""),
            verbose=True,
            memory=False,
            llm=self.llm,
            max_iter=2,
            tools=[SearchTools().search_internet],
            allow_delegation=True

        )

    # def news_analyzer_agent(self):
    #    """Agent to analyze the fetched infoes."""
#
    #    return Agent(
    #        role='News Analyzer',
    #        goal=dedent(f"""\
    #            Analyzes each information, story and element and generates
    #            a cohesive, readable and detailed summary in markdown about {self.climber_name}"""),
#
    #        backstory=dedent("""\
    #            With a keen analytical mind and a knack for distilling complex
    #            information, you turn raw data into in-depth analyses of the successes
    #            and details of the story's protagonist's life, making them accessible
    #            and engaging to our audience."""),
#
    #        tools=[SearchTools.search_internet],
    #        verbose=True,
    #        memory=True,
    #        llm=self.llm,
    #        max_iter=2,
    #        allow_delegation=False
    #    )
