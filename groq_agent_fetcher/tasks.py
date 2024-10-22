
"""tasks for AI assistant"""
from textwrap import dedent
from typing import List, Dict, Optional
from crewai import Task
from pydantic import BaseModel
from tools.search_tools import SearchTools


class ClimberProfile(BaseModel):
    """json structure for infoes collection"""
    name: str
    early_life: Dict[str, str]
    career_highlights: Dict[str, str]
    notable_ascents: Optional[List[Dict[str, str]]] = None
    achievements: Optional[List[Dict[str, str]]] = None
    philosophy: Dict[str, str]
    personal_life: Dict[str, str]
    legacy: Dict[str, str]
    tragedy: Optional[Dict[str, str]] = None
    quotes: List[Dict[str, str]]
    urls: List[str]


class ClimbingNewsletterTasks():
    """series of tasks for newsletter writing"""

    def __init__(self):

        # Define 'newline' as a class attribute
        self.newline = "\n"
        self.climber_name = "Patrick Edlinger"  # Store the climber's name
        self.search_tools = SearchTools()

    def fetch_info(self, query: str) -> Dict[str, str]:
        """Fetch information and URL using the search tool"""
        results = self.search_tools.search_internet(query)
        if isinstance(results, str):
            return {"description": results, "url": ""}
        top_result = results[0] if results else {
            "title": "No result", "link": "", "snippet": ""}
        return {"description": top_result["snippet"], "url": top_result["link"]}

    def fetch_news_task(self, agent, callback_function):
        """Find EXISTING, verified, relevant, and quality information about the specified climber."""

        # Define a condition for tragedy, for example, setting it to True for the test
        some_condition = True

        # Fetch information from the web with associated URLs
        early_life_info = self.fetch_info(f"{self.climber_name} early life")
        career_highlights_info = self.fetch_info(
            f"{self.climber_name} career highlights")
        notable_ascents_info = [self.fetch_info(
            f"{self.climber_name} notable ascent {i+1}") for i in range(6)]
        achievements_info = [self.fetch_info(
            f"{self.climber_name} achievement {i+1}") for i in range(6)]
        philosophy_info = self.fetch_info(f"{self.climber_name} philosophy")
        personal_life_info = self.fetch_info(
            f"{self.climber_name} personal life")
        legacy_info = self.fetch_info(f"{self.climber_name} legacy")
        tragedy_info = self.fetch_info(
            f"{self.climber_name} tragedy") if some_condition else None
        quotes_info = [self.fetch_info(
            f"{self.climber_name} quote {i+1}") for i in range(3)]

        task_description = ClimberProfile(
            name=self.climber_name,
            early_life={
                "description": early_life_info["description"], "url": early_life_info["url"]},
            career_highlights={
                "description": career_highlights_info["description"], "url": career_highlights_info["url"]},
            notable_ascents=[{"route": info["description"], "date": "", "style": "",
                              "grade": "", "url": info["url"]} for info in notable_ascents_info],
            achievements=[{"award": info["description"], "year": "",
                           "reason": "", "url": info["url"]} for info in achievements_info],
            philosophy={
                "description": philosophy_info["description"], "url": philosophy_info["url"]},
            personal_life={
                "description": personal_life_info["description"], "url": personal_life_info["url"]},
            legacy={
                "description": legacy_info["description"], "url": legacy_info["url"]},
            tragedy={"description": tragedy_info["description"],
                     "url": tragedy_info["url"]} if tragedy_info else None,
            quotes=[{"quote": info["description"], "url": info["url"]}
                    for info in quotes_info],
            urls=[early_life_info["url"], career_highlights_info["url"]] + [info["url"]
                                                                            for info in notable_ascents_info + achievements_info + quotes_info if info["url"]]
        )

        return Task(
            description=dedent(f"""\
                Fetch and refine valuable information about {self.climber_name}.
                Your output is the first brick to reach the final goal;
                the next task depends on the quality of your output,
                so enter only EXISTING, verified, quality urls and information.
                Do your best!
            """),
            agent=agent,
            async_execution=True,
            expected_output=dedent(f"""\
                It is very impoprtant that the format of the output follows the pattern shown in task_description.
                Here the template: {task_description}"""),
            callback=callback_function
        )

    # def analyze_news_task(self, agent, context, callback_function):
    #    """Analyze the collected news data and format it in Markdown"""
#
    #    # Genera il contenuto Markdown
    #    markdown_output = dedent(f"""\
    #        # Climber Profile: {self.climber_name}
#
    #        ## Early Life and Career
    #        Collection of info related to the life and career of {self.climber_name}.
    #        Insert valuable dictation useful to the story and introduction of the subject.
#
    #        ## Introduction
    #        A rich introduction to the climber, the details that distinguished him, the values he conveyed in the climbing community, and a couple of biographical anecdotes.
#
#
    #        ## Notable Ascents
    #        List the climber's key achievements:
    #        (enrich it with all the details useful for a narrative, for example, climbers like to know the environmental conditions, the degrees of difficulty, and the spirit with which the feat was approached)
    #        - Description of the ascent. Summary of any anecdote about the feat of the ascent of the route.
    #        - Description of the ascent. Summary of any anecdote about the feat of the ascent of the route.
#
#
    #        ## Awards and Recognition
    #        Detail the major awards and titles won by the climber:
    #        - Name of the award. Summary of any anecdote about the feat of the award.
    #        - Name of the award. Summary of any anecdote about the feat of the award.
#
    #        ## Personal Life
    #        Discuss any relevant details about their personal life that are publicly known.
#
#
    #        ## Tragic End (Only if the research subject is dead)
    #        Narrate the circumstances of their untimely demise on 'death_date', emphasizing the impact on the climbing community.
#
    #        ## Legacy
    #        Conclude with a reflection on their legacy and continuing influence in the sport.
    #    """)
#
    #    return Task(
    #        description=dedent(f"""\
    #            Thoroughly analyze the context provided by the previous task and extract
    #            valuable information rich in details critical to creating a compelling and exciting newsletter.
    #            It is very important to follow the pattern shown in markdown_output.
    #            Here the template:\
    #                {markdown_output} """),
#
    #        agent=agent,
    #        context=context,
#
    #        expected_output=dedent("""\
    #            Saving a very good output formatted in Markdown."""),
#
    #        callback=callback_function
    #    )
