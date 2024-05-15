
"""tasks for AI assistant"""
from textwrap import dedent
from typing import List
from crewai import Task
from pydantic import BaseModel



class ClimberProfile(BaseModel):
    name: str
    url: str
    summary: str
    notable_ascents: List[dict]
    awards: List[dict]
    personal_life: str
    quotes: List[str]



class ClimbingNewsletterTasks():
    """series of tasks for newsletter writing"""

    def __init__(self):

        # Definisci 'newline' come attributo di classe
        self.newline = "\n"
        self.climber_name = "Patrick Edlinger"  # Store the climber's name
        self.output_fetch_path = "C:/Users/user/Desktop/CODing/crew_AI/heirerchal_process/groq_experiment/risultato/fetch.txt"
        self.output_analyze_path = "C:/Users/user/Desktop/CODing/crew_AI/heirerchal_process/groq_experiment/risultato/analyze.md"
        self.output_compile_path = "C:/Users/user/Desktop/CODing/crew_AI/heirerchal_process/groq_experiment/risultself.ato"

#        self.last_request_time = time.time()
#        self.min_interval_seconds = 60  # Minimum interval between requests

#    def _ensure_rate_limit(self):
#        """Ensure that the task execution respects the rate limit"""
#        current_time = time.time()
#        elapsed_time = current_time - self.last_request_time
#        if elapsed_time < self.min_interval_seconds:
#            logging.debug("Rate limit hit, sleeping for %sself.min_interval_seconds - %selapsed_time seconds")
#            time.sleep(self.min_interval_seconds - elapsed_time)
#        self.last_request_time = time.time()
#        logging.debug("Continuing execution after rate limit wait")

    def fetch_news_task(self, agent):
        """Fetch relevant info on climbing for a specified climber."""

#        self._ensure_rate_limit()

        task_description = ClimberProfile(
            name=self.climber_name,
            url="https://specific-climber-profile.com",
            summary="A brief overview highlighting key aspects of the career of the climber.",
            notable_ascents=[
                {"route": "The Nose, El Capitan", "date": "June 1998", "style": "Free solo", "grade" : "8b+"},
                {"route": "La Dura Dura, Oliana", "date": "January 2013", "style": "Lead climbing"}
            ],
            awards=[{"award": "Golden Piton", "year": "2004", "reason": "Outstanding achievements in sport climbing"}],
            personal_life="Details about the early life of climber, interests, and other non-climbing activities.",
            quotes=["Climbing is not a battle with the elements, nor against the law of gravity. It's a battle against oneself."]
        )


        return Task(
            description=dedent(f"""Gather and refine valuable information about {self.climber_name}.
                Remember that your output is the first brick to reach the final goal,
                so the quality of your next job depends on the quality of your work, so do your best!
            """),
            agent=agent,
            async_execution=True,
            expected_output=f"""It is very impoprtant that the format of the output follows the pattern shown in task_description.
                Here the template: {task_description}""",
            output_file=self.output_fetch_path
        )

    def analyze_news_task(self, agent, context):
        """Analyze the collected news data and format it in Markdown."""

#        self._ensure_rate_limit()

        # Genera il contenuto Markdown
        markdown_output = dedent(f"""
            # Climber Profile: {self.climber_name}

           ## Early Life and Career
            {self.climber_name}, born on 20/01/1975 in Italy , began climbing at the age of 13. Highlight their early influences and initial accomplishments.


            ## Introduction
            A rich introduction to the climber, the details that distinguished him, the values he conveyed in the climbing community, and a couple of biographical anecdotes.


            ## Notable Ascents
            List the climber's key achievements:
            (enrich it with all the details useful for a narrative, for example, climbers like to know the environmental conditions, the degrees of difficulty, and the spirit with which the feat was approached)
            - Description of the ascent.
            - Description of the ascent.


            ## Awards and Recognition
            Detail the major awards and titles won by the climber:
            - Golden Piton in 2004
            - Piolets d'Or in 2006

            ## Personal Life
            Discuss any relevant details about their personal life that are publicly known.

            ## Tragic End
            Narrate the circumstances of their untimely demise on 'death_date', emphasizing the impact on the climbing community.

            ## Legacy
            Conclude with a reflection on their legacy and continuing influence in the sport.
        """)


        return Task(
            description=dedent(f"""Thoroughly analyze the context provided by the previous task and extract
                valuable information rich in details critical to creating a compelling and exciting newsletter.
                It is very important to follow the pattern shown in markdown_output.
                Here the template: {markdown_output} """),
            agent=agent,
            context=context,
            expected_output="Markdown formatted output saved.",
            output_file=self.output_analyze_path
        )

    def compile_newsletter_task(self, agent, context):
        """Compile the analyzed climbing information into a styled markdown newsletter."""

#        self._ensure_rate_limit()

        # Creare la newsletter con un'intestazione e una struttura chiara
        newsletter_content = dedent(f"""
            # This Month's Climbing Icon: {self.climber_name}{self.newline}{self.newline}
            # {self.climber_name}: A Legendary French Rock Climber{self.newline}{self.newline}
            **Early Life and Career**{self.newline}
            {self.climber_name} was a French rock climber born on June 15, 1960, in Dax, France. He began climbing at the age of 12 and quickly made a name for himself in the climbing community.{self.newline}{self.newline}
            **Notable Ascents**{self.newline}
            - **La danse des Balrogs**: {self.climber_name} made the first ascent of this 8c route in 1989, which was considered one of the most difficult climbs at the time.{self.newline}
            - **Agincourt**: He made the first ascent of this 8b+ route in 1986, a significant achievement in the climbing world.{self.newline}{self.newline}
            **Awards and Recognition**{self.newline}
            - **Piolet d'Or**: {self.climber_name} was awarded the Piolet d'Or, a prestigious award for mountaineering, in 1992.{self.newline}
            - **French National Climbing Champion**: He won the French National Climbing Championship multiple times throughout his career.{self.newline}{self.newline}
            **Personal Life**{self.newline}
            {self.climber_name} was married and had two children. Tragically, he died on November 16, 2012, at the age of 52, in a climbing accident in the Vercors region of France.{self.newline}{self.newline}
            **Legacy**{self.newline}
            {self.climber_name}'s legacy in the climbing world is undeniable. He was known for his bold and dynamic climbing style, which inspired many climbers around the world. His achievements and contributions to the sport of climbing will always be remembered and celebrated.{self.newline}{self.newline}
            **His Legacy:** {self.climber_name} continues to inspire new generations of climbers around the world...{self.newline}{self.newline}
        """)


        return Task(
            description="""Use the provided context to compile and format the newsletter in Markdown;
                include enough information to be able, in the next task, to write a 2000-word article,
                so it will be useful to take full advantage of the context. The work done is essential for
                a quality end result, so commit to providing the best context for the next task.""",
            agent=agent,
            context=context,
            expected_output=dedent(f"""A complete newsletter in markdown format, ready for final article
                composition. It is very important to follow the pattern shown in newsletter_content.
                Here the template: {newsletter_content} """),
            output_file=self.output_compile_path
        )


    def write_story_task(self, agent, context, callback_function):
        """Final writer of the newsletter story about a climber's iconic exploits."""

#        self._ensure_rate_limit()

        return Task(
            description=f"""Using the detailed content provided by the "context",
                create an engaging and inspiring story that captures the essence of the results and the story of {self.climber_name}.
                The story should be structured with about 2,000 words, and should include:

                - An engaging introduction that draws the reader in.
                - A narrative details one or two climbs; enrich with details such as difficulty grades, environmental conditions, context.
                - Personal details, trivia and anecdotes.
                - Descriptions that bring climbs and experiences to life.
                - Interesting conclusions that reflect on the mountaineer's legacy and impact on the community.

                The narrative should be well paced, using a conversational but structured style to make the content relatable and impactful.""",
            agent=agent,
            context=context,
            async_execution=False,

            expected_output="""A perfectly packaged story in TEXT FORMAT, ready to be
                included in the weekly newsletter. The story should be structured with about 2,000 words, must be inspirational,
                using a practical language style to connect deeply with readers.
                Remember to respect the details in 'description' and enrich the story with details provided by the context""",
            callback=callback_function
        )


  #  Try to tell an epic feat or two from {self.climber_name}'s life, e.g., take advantage
  #              of the info that shows the name and grade of a route and talk about it!
  #              Climbers really like to know the names and difficulty grades.