
"""definizione assistente AI"""
import os
from textwrap import dedent
from crewai import Agent
from langchain_groq import ChatGroq
#from langchain.agents import load_tools
from tools.search_tools import SearchTools


# Human Tools
#human_tools = load_tools(["human"])


class ClimbingNewsletterAgents():
    """Definition of agents for managing climbing newsletter"""

    def __init__(self, climber_name):
        ## Istanze LLM

   #     llama3_8b = "llama3-8b-8192"
   #     llama3_70b = "llama3-70b-8192"

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        self.climber_name = climber_name  # Store the climber's name
#        self.token_limit_per_minute = 2890
#        self.token_usage = 0
#
#    def _reset_token_usage(self):
#        """Reset the token usage counter every minute"""
#        self.token_usage = 0
#
#    def check_token_limit(self, tokens_required):
#        if self.token_usage + tokens_required > self.token_limit_per_minute:
#            logging.error("Token limit exceeded, waiting...")
#            # Implementare un metodo di pausa o riprova
#            time.sleep(60)  # Potrebbe essere necessario un approccio più sofisticato
#            self._reset_token_usage()
#        else:
#            self.token_usage += tokens_required

    def editor_agent(self):
        """supervising editor agent"""

#        self.check_token_limit(500)  # Assuming an average token estimate per operation

        return Agent(
            role='Editor',
            goal=dedent("""\
                Oversee the creation of the climbing sports newsletter"""),
            backstory=dedent("""\
                With a keen eye for detail and a passion for storytelling
                in climbing sports, you ensure that the newsletter not only informs but
                also engages and inspires the climbing community. """),
            allow_delegation=True,
            verbose=True,
            llm=self.llm,
            memory=True,
            max_iter=2
        )
    def news_fetcher_agent(self):
        """Agent to fetch basic information"""
#        try:
#            self.check_token_limit(500)
        return Agent(
            role='News Fetcher',
            goal=dedent(f"""\
                Research and fetch detailed stories and biographical
                elements of iconic climber: {self.climber_name}"""),
            backstory=dedent("""\
                As a dedicated researcher of climbing history, you delve into
                archives and current records to bring the most compelling and detailed stories
                to light."""),
            verbose=True,
            memory=True,
            llm=self.llm,
            max_iter=2,
            tools=[SearchTools.search_internet],
            allow_delegation=True
        )
#        except Exception as e:
#            logging.error(f"Failed to create news_fetcher_agent: {e}")
#            return None

    def news_analyzer_agent(self):
        """infos analyzer agent"""

#        self.check_token_limit(500)

        return Agent(
            role='News Analyzer',
            goal=dedent(f"""\
                Analyzes each information, story and element and generates
                a cohesive, readable and detailed summary in markdown about {self.climber_name}"""),

            backstory=dedent("""\
                With a keen analytical mind and a knack for distilling complex
                information, he transforms raw data into in-depth analyses of the successes
                and details of the story's protagonist's life, making them accessible and
                engaging to our audience."""),

            tools=[SearchTools.search_internet],
            verbose=True,
            memory=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=True
        )

    def newsletter_compiler_agent(self):
        """agent compiling newsletter for final writer"""

#        self.check_token_limit(500)

        return Agent(
            role='Newsletter Compiler',
            goal=dedent("""\
                Compile the analyzed informations into a final newsletter format"""),
            backstory=dedent("""\
                As the architect of the newsletter, you will need to meticulously
                organize and format the content, ensuring a consistent and fuctional presentation
                to ensure the Storyteller's development of the final story. Be sure to follow the
                newsletter format guidelines and maintain consistency."""),
            verbose=True,
            memory=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=True  # Writers may prefer to have full control over the final output

        )

    def storyteller_agent(self):
        """final writer agent"""

#        self.check_token_limit(500)
        return Agent(
            role="Storyteller",
            goal=dedent("""\
                Write an engaging true story for the blog's climbing newsletter.
                """),
            backstory=dedent("""\
                As an experienced writer with a passion for climbing, you are able to
                create compelling narratives that captivate readers and highlight the human aspect
                of climbing adventures. You avoid writing predictable and trite articles;
                rather, you enrich them with details that totally immerse the reader in the story."""),
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=False  # Writers may prefer to have full control over the final output
        )
