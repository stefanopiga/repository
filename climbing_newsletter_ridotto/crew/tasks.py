
"""tasks for AI assistant"""
from functools import partial
import json
from textwrap import dedent
from crewai import Task
from config import llm_gpt4, llm_gpt3_5


class ClimbingNewsletterTasks():
    """series of tasks for newsletter writing"""
    def fetch_news_task(self, agent, climber_name):
        """fetch relevant info on climbing"""

        climber_profile = {
                "name": climber_name,
                "url": "https://specific-climber-profile.com",
                "summary": "A brief overview highlighting key aspects of the career of the climber.",
                "notable_ascents": [
                    {
                        "route": "The Nose, El Capitan",
                        "date": "June 1998",
                        "style": "Free solo"
                    },
                    {
                        "route": "La Dura Dura, Oliana",
                        "date": "January 2013",
                        "style": "Lead climbing"
                    }
                ],
                "awards": [
                    {
                        "award": "Golden Piton",
                        "year": "2004",
                        "reason": "Outstanding achievements in sport climbing"
                    }
                ],
                "personal_life": "Details about the early life of climber, interests, and other non-climbing activities.",
                "quotes": [
                    "Climbing is not a battle with the elements, nor"
                    "against the law of gravity. It is a battle against oneself."
                ]
                }

        json_output = json.dumps([{"climber_profile": climber_profile}], indent=4)

        return Task(
            description=dedent(f"""research and gather detailed information
                               about an {climber_name} sporting achivement,
                               including biographical elements, the URL from which the news came, notable climbs,
                               awards,contributions, personal life, and quotes."""),
            agent=agent,
            async_execution=True,
            expected_output = dedent(f"""\
                A list of detailed biographical elements, URLs, and climbing achievements of {climber_name}.
                Example Output (format):
                {json_output}
            """)
        )

    def analyze_news_task(self, agent, context, climber_name):
        """info analysis and summaries for further work"""
        return Task(
            description='Carefully analyse data and ensure the article is well formatted',
            agent=agent,
            async_execution=True,
            context=context,
            expected_output=dedent(f"""An analysis in markdown format, including a summary, detailed
                points, and a 'Why it is relevant' section.analyze only information relevant to {climber_name}. The article must follow the
                correct format.

                ## Climber Profile: {climber_name}

                **The Rundown:**
                - **Name**: {climber_name}
                - **Notable Climbs**: [List notable climbs]
                - **Awards**: [List awards]

                **The Details:**
                [Provide detailed analysis here, such as notable ascents and awards]

                **Why it Matters:**
                - **Influence on Sport**: [Describe influence on climbing sport]
                - **Quotes**: [List relevant quotes]

                This format should be strictly followed to ensure consistency and clarity in the presentation of climber profiles.
                """)
        )


    def compile_newsletter_task(self, agent, context):
        """Compilation of a list for the final writer"""
        return Task(
            description="""Compile the newsletter""",
            agent=agent,
            async_execution=True,
            context=context,
            expected_output="""A complete newsletter in markdown format, with a consistent style
                and layout, using the analyzed information.
                Example Output:
                '# This Month's Climbing Icon: Lynn Hill\\n\\n
                **Who is Lynn Hill?**\\n\\n
                Lynn Hill, a legend in the climbing community, redefined what is possible in the sport...\\n\\n
                **Climbing The Nose:** A story of resilience and vision...\\n\\n
                **Her Legacy:** Lynn continues to inspire new generations of climbers around the world...\\n\\n
            """
        )


    def write_story_task(self, agent, context, callback_function):
        """scrittore finale della newsletter"""
        return Task(
            description="""Using the results provided, write a complete and true story that
                engages the readers for about eight minutes, so about three thousand words.""",
            agent=agent,
            async_execution=False,
            context=context,
            expected_output="""A perfectly packaged story ready for inclusion in the blog for the
                weekly newsletter readers' meeting IN MARKDOWN FORMAT.
            """,
            callback=callback_function

        )
