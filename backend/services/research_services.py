from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from models.research import ResearchRequest, ResearchResponse
from databases.mongodb import insert_research
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from serpapi import GoogleSearch

load_dotenv()

# Initialize SerpAPI and LLM
serpapi = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    model="gpt-3.5-turbo"  # Specify the model name as required by Azure
)


# Prompt template for summarizing findings
summary_prompt = PromptTemplate(
    input_variables=["topic", "search_results"],
    template="""
    You are a research assistant. Summarize the following search results for the topic '{topic}' in a concise paragraph (200-250 words). Ensure the summary is clear, informative, and covers key points from the results. Cite sources by number [1], [2], etc., corresponding to the source list provided.

    Search Results:
    {search_results}
    """
)

# Create RunnableSequence for summarization
summary_chain = summary_prompt | llm

def perform_research(request: ResearchRequest, user_id: str) -> ResearchResponse:
    # Perform web search
    search_results, sources = perform_web_search(request.topic, request.max_results)
    
    
    # Generate summary
    summary = summary_chain.invoke(
        {"topic": request.topic, "search_results": search_results}
    ).content
    
    # Store in MongoDB with user_id
    research_data = {
        "topic": request.topic,
        "summary": summary.strip(),
        "sources": sources,
        "created_at": datetime.utcnow(),
        "user_id": user_id
    }
    research_id = insert_research(research_data, user_id)
    
    return ResearchResponse(
        topic=request.topic,
        summary=summary.strip(),
        sources=sources,
        research_id=research_id
    )

# def perform_web_search(topic: str, max_results: int) -> tuple[str, List[Dict[str, str]]]:
#     search_results = serpapi.run(topic, num_results=max_results)
#     print("Type of search results: ",type(search_results))
#     print(search_results)
#     formatted_results = ""
#     sources = []
    
#     for idx, result in enumerate(search_results.get("organic_results", []), 1):
#         title = result.get("title", "No title")
#         snippet = result.get("snippet", "No snippet")
#         link = result.get("link", "#")
        
#         formatted_results += f"[{idx}] {title}: {snippet}\n"
#         sources.append({
#             "source_id": str(idx),
#             "title": title,
#             "link": link
#         })
    
#     return formatted_results, sources

def perform_web_search(topic: str, max_results: int) -> tuple[str, List[Dict[str, str]]]:
    try:
        # Configure SerpAPI search
        params = {
            "q": topic,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": max_results
        }
        search = GoogleSearch(params)
        search_results = search.get_dict()
        
        print("Type of search results: ", type(search_results))
        print("Raw search results keys: ", list(search_results.keys()))
        
        formatted_results = ""
        sources = []
        
        # Handle dictionary response with organic_results
        if isinstance(search_results, dict):
            for idx, result in enumerate(search_results.get("organic_results", [])[:max_results], 1):
                title = result.get("title", "No title")
                snippet = result.get("snippet", "No snippet")
                link = result.get("link", "#")
                
                formatted_results += f"[{idx}] {title}: {snippet}\n"
                sources.append({
                    "source_id": str(idx),
                    "title": title,
                    "link": link
                })
            
            # Optionally include AI overview if present
            if "ai_overview" in search_results and search_results["ai_overview"]:
                ai_content = search_results["ai_overview"].get("content", "")
                if ai_content:
                    formatted_results += f"[AI Overview]: {ai_content}\n"
        
        return formatted_results, sources
    
    except Exception as e:
        print(f"Error in web search: {str(e)}")
        return "", []  # Return empty results on error