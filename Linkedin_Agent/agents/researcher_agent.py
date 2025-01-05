from crewai import Agent
from langchain.retrievers import TavilySearchAPIRetriever
from langchain.tools import Tool


class ResearcherAgent:
    def __init__(self, tavily_api_key,llm):
        self.search = TavilySearchAPIRetriever(
            api_key=tavily_api_key,
            k=5  # Number of results to return
        )
        self.llm = llm

    def create(self):
        # Create a tool from the research_topic method
        research_tool = Tool(
            name="Research Topic",
            func=self.research_topic,
            description="Searches for information about a given topic using Tavily"
        )

        return Agent(
            role='Research Analyst',
            goal='Research trending topics and create comprehensive content briefs',
            backstory="""You are an expert content researcher with deep knowledge of 
            professional trends and LinkedIn content strategies. Your goal is to identify 
            engaging topics and create detailed content briefs.""",
            llm=self.llm,
            tools=[research_tool],
            verbose=True
        )

    async def research_topic(self, topic: str) -> str:
        """Research a specific topic using Tavily Search"""
        try:
            # Perform the search
            search_results = self.search.invoke(topic)
            
            # Format the research results
            research_summary = "Research findings:\n\n"
            for i, doc in enumerate(search_results, 1):
                research_summary += f"{i}. {doc.page_content}\n\n"
            
            # Add source URLs
            research_summary += "\nSources:\n"
            for i, doc in enumerate(search_results, 1):
                if doc.metadata.get('source',None) != None:
                    research_summary += f"- {doc.metadata['source']}\n"
            print(research_summary)
            return research_summary

        except Exception as e:
            print(f"Error in research: {str(e)}")
            return f"Error during research: {str(e)}"