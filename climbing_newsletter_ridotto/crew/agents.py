
"""definizione assistente AI"""
from textwrap import dedent
from crewai import Agent
from langchain.agents import load_tools
from tools.search_tools import SearchTools
from config import llm_gpt4, llm_gpt3_5

# Human Tools
human_tools = load_tools(["human"])

class ClimbingNewsletterAgents():
    """definizione degli agenti"""
    def editor_agent(self):
        """agente di supervisione"""
        return Agent(
            role='Editor',
            goal='Oversee the creation of the climbing sports newsletter',
            backstory="""With a keen eye for detail and a passion for storytelling
            in climbing sports, you ensure that the newsletter not only informs but
            also engages and inspires the climbing community. """,
            allow_delegation=True,
            llm=llm_gpt4,
            verbose=True,
            memory=True,
            max_iter=15
        )
    def news_fetcher_agent(self, climber_name):
        """agente di raccolta info base"""
        return Agent(
            role='NewsFetcher',
            goal=dedent(f"""Research and fetch detailed stories and biographical
                elements of iconic climber: {climber_name}"""),
            verbose=True,
            memory=True,
            llm=llm_gpt3_5,
            backstory=("""As a dedicated researcher of climbing history, you delve into
            archives and current records to bring the most compelling and detailed stories
            to light."""),
            tools=[SearchTools.search_internet],
            allow_delegation=True
        )

    def news_analyzer_agent(self, climber_name):
        """agente che analizza info"""
        return Agent(
            role='NewsAnalyzer',
            goal=dedent(f"""Analyzes each information, story and element and generates
                a cohesive, readable and detailed summary in markdown about {climber_name}"""),

            backstory=("""With a keen analytical mind and a knack for distilling complex
                information, he transforms raw data into in-depth analyses of the successes
                and details of the story's protagonist's life, making them accessible and
                engaging to our audience."""),

            tools=[SearchTools.search_internet],
            verbose=True,
            memory=True,
            llm=llm_gpt3_5,
            allow_delegation=True
        )

    def newsletter_compiler_agent(self):
        """agente che compila la newsletter per lo scrittore finale"""
        return Agent(
            role='NewsletterCompiler',
            goal='Compile the analyzed informations into a final newsletter format',
            backstory=("""As the architect of the newsletter, you will need to meticulously
                organize and format the content, ensuring a consistent and fuctional presentation
                to ensure the Storyteller's development of the final story. Be sure to follow the
                newsletter format guidelines and maintain consistency."""),
            verbose=True,
            memory=True,
            llm=llm_gpt3_5,
            allow_delegation=True  # Writers may prefer to have full control over the final output
        )

    def storyteller_agent(self):
        """agente scrittore finale"""
        return Agent(
            role='Storyteller',
            goal='Writing true and engaging stories for the climbing newsletter',
            backstory="""As an experienced writer with a passion for climbing, you are able to
                create compelling narratives that captivate readers and highlight the human aspect
                of climbing adventures.""",
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=llm_gpt4,
            allow_delegation=False  # Writers may prefer to have full control over the final output
        )
