import os
from dotenv import load_dotenv
from crewai import Crew, Task, LLM
from groq import Groq
from linkedin_api import Linkedin

from agents.researcher_agent import ResearcherAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent
from agents.poster_agent import PosterAgent

class LinkedInContentCrew:
    def __init__(self):
        load_dotenv()
        
        # Initialize clients
        tavily_api_key = os.getenv('TAVILY_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.linkedin_client = Linkedin(
            os.getenv('LINKEDIN_EMAIL'),
            os.getenv('LINKEDIN_PASSWORD')
        )
        #self.llm = LLM("groq/llama-3.3-70b-versatile")
        self.llm = LLM("openai/gpt-4o-mini",api_key=os.getenv('OPENAI_API_KEY'))

        # Initialize agents
        self.researcher = ResearcherAgent(tavily_api_key, self.llm).create()
        self.writer = WriterAgent(self.groq_api_key, self.llm).create()
        self.reviewer = ReviewerAgent(self.groq_api_key, self.llm).create()
        self.poster = PosterAgent(self.linkedin_client, self.llm).create()

    def create_content(self, topic):
        """Create LinkedIn content without posting"""
        # Define research and writing tasks
        research_task = Task(
            description=f"Research this topic thoroughly: {topic}",
            agent=self.researcher,
            expected_output="Detailed research findings including key insights, trends, and statistics about the topic"
        )

        writing_task = Task(
            description="Create an engaging LinkedIn post from the research",
            agent=self.writer,
            expected_output="A well-crafted LinkedIn post under 1300 characters with hashtags, engaging emojis and clear call-to-actions"
        )

        review_task = Task(
            description="Review and optimize the LinkedIn post for maximum impact",
            agent=self.reviewer,
            expected_output="A refined and optimized version of the post with improved engagement potential while maintaining professionalism only and no furtherreasoning or explanation"
        )

        posting_task = Task(
            description="Post the content to LinkedIn",
            agent=self.poster,
            expected_output="Confirmation that the post was successfully published to LinkedIn along with the URL of the post"
        )

        # Create and run content creation crew
        content_crew = Crew(
            agents=[self.researcher, self.writer, self.reviewer],
            tasks=[research_task, writing_task, review_task]
        )

        return content_crew.kickoff()

    def post_content(self, content):
        """Post the created content to LinkedIn"""
        posting_task = Task(
            description="Post the content to LinkedIn",
            agent=self.poster,
            expected_output="Confirmation that the post was successfully published to LinkedIn along with the URL of the post"
        )

        # Create and run posting crew
        posting_crew = Crew(
            agents=[self.poster],
            tasks=[posting_task]
        )

        return posting_crew.kickoff()

    def run(self, topic):
        """Complete workflow: Create and post content"""
        # First create the content
        print("\nPhase 1: Creating and reviewing LinkedIn content...")
        content = self.create_content(topic)
        print("\nContent created and reviewed successfully!")
        print(f"Inside run function content['content'] : {content}")
        # # Then post it
        # print("\nPhase 2: Posting to LinkedIn...")
        # result = self.post_content(content)
        # print("\nPosting completed!")
        
        return {
            'content': content,
            #'posting_result': result
        } 