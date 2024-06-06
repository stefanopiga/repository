
"""tasks for AI assistant"""
from textwrap import dedent
from typing import List, Dict, Optional
from crewai import Task
from pydantic import BaseModel


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

        # Definisci 'newline' come attributo di classe
        self.newline = "\n"
        self.climber_name = "Patrick Edlinger"  # Store the climber's name

    def fetch_news_task(self, agent, callback_function):
        """Find EXISTING, verified, relevant, and quality information about the specified climber."""

        initial_ascent = {"route": "", "date": "", "style": "", "grade": ""}
        initial_achievement = {"award": "", "year": "", "reason": ""}
        task_description = ClimberProfile(
            name=self.climber_name,
            early_life={"description": "", "url": ""},
            career_highlights={"description": "", "url": ""},
            notable_ascents=[initial_ascent.copy() for _ in range(6)],

            achievements=[initial_achievement.copy() for _ in range(6)],

            philosophy={"description": "", "url": ""},
            personal_life={"description": "", "url": ""},
            legacy={"description": "", "url": ""},
            # Specifica None se non c'è tragedia
            tragedy={"description": "", "url": ""},
            quotes=[{"quote": "", "url": ""}],
            urls=[]
        )

        # Add the sources used to collect the information
        # You can add URLs to this list
        task_description.urls.extend([
            "https://example.com/early_life",
            "https://example.com/career_highlights",
            "https://example.com/notable_ascent1",
            # Add more sources here
        ])

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
