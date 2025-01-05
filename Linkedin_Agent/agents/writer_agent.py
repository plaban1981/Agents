from crewai import Agent
from langchain_groq import ChatGroq
from langchain.tools import Tool

class WriterAgent:
    def __init__(self, groq_api_key, llm):
        self.groq_llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.1-8b-instant",
            groq_api_key=groq_api_key,
            max_tokens=1000
        )
        self.llm = llm

    def create(self):
        writing_tool = Tool(
            name="Write LinkedIn Post",
            func=self.write_post,
            description="Creates an engaging LinkedIn post from research findings"
        )

        return Agent(
            role='Content Writer',
            goal="""Create engaging LinkedIn posts from research briefs.
            Create a LinkedIn post based on this research:{research_brief}
        
        Follow these guidelines:
        - Keep it under 2000 characters
        - Include relevant hashtags
        - Use engaging hooks
        - Add engaging emojis
        - Add clear call-to-actions
        - Format with appropriate line breaks
        - Make it professional and thought-provoking
        - Add reference URLs if any in the {research_brief}""",
            backstory="""You are an expert LinkedIn content creator who knows 
            how to craft viral, engaging posts that drive professional discussions.
            Your goal is to create content that resonates with professionals and 
            generates meaningful engagement.""",
            llm=self.llm,
            #tools=[writing_tool],
            verbose=True
        )

    async def write_post(self, research_brief: str) -> str:
        """Transform research brief into LinkedIn post"""
        prompt = f"""Create a LinkedIn post based on this research:
        {research_brief}
        
        Follow these guidelines:
        - Keep it under 1300 characters
        - Include relevant hashtags
        - Use engaging hooks
        - Add engaging emojis
        - Add clear call-to-actions
        - Format with appropriate line breaks
        - Make it professional and thought-provoking"""

        response = await self.groq_llm.ainvoke(prompt)
        print("\nGenerated LinkedIn post:")
        print(response.content)
        return response.content 