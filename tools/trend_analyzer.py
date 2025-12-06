"""Trend analysis tool for identifying trending topics and content opportunities."""

from langchain.tools import tool
from tavily import TavilyClient
import os
from typing import Dict, Any
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _get_tavily_client():
    """Get Tavily client with API key."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    return TavilyClient(api_key=api_key)


@tool
def analyze_trends_tool(topic: str, industry: str = "general") -> str:
    """
    Analyze current trends related to a specific topic or industry.
    
    Args:
        topic: The topic or keyword to analyze trends for
        industry: The industry context (e.g., 'technology', 'marketing', 'health')
    
    Returns:
        JSON string with trending topics, search volume insights, and content opportunities
    """
    try:
        client = _get_tavily_client()
        
        if client:
            # Use Tavily to find trending content
            query = f"trending {topic} {industry} latest news trends"
            results = client.search(
                query=query,
                max_results=10,
                search_depth="advanced",
                include_raw_content=False
            )
            
            trends = []
            for result in results.get("results", []):
                trends.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", "")[:200],
                    "published": result.get("published_date", ""),
                    "relevance_score": result.get("score", 0)
                })
            
            analysis = {
                "topic": topic,
                "industry": industry,
                "analyzed_at": datetime.now().isoformat(),
                "trending_topics": trends,
                "insights": {
                    "total_results": len(trends),
                    "high_relevance_count": sum(1 for t in trends if t["relevance_score"] > 0.7),
                    "content_opportunities": [
                        "Create how-to guides based on trending questions",
                        "Develop comparison content for popular alternatives",
                        "Write opinion pieces on controversial trends",
                        "Produce case studies featuring successful implementations"
                    ]
                }
            }
        else:
            # Fallback: Mock trend analysis
            analysis = {
                "topic": topic,
                "industry": industry,
                "analyzed_at": datetime.now().isoformat(),
                "trending_topics": [
                    {
                        "title": f"Latest developments in {topic}",
                        "snippet": f"Recent advancements and trends in {topic} within the {industry} industry",
                        "relevance_score": 0.85
                    },
                    {
                        "title": f"How {topic} is transforming {industry}",
                        "snippet": f"Analysis of {topic}'s impact on the {industry} sector",
                        "relevance_score": 0.78
                    }
                ],
                "insights": {
                    "note": "Using fallback mode - install Tavily for real-time trend data",
                    "content_opportunities": [
                        f"Write comprehensive guides about {topic}",
                        f"Create comparison content for {topic} solutions",
                        f"Develop {industry}-specific use cases for {topic}",
                        f"Produce expert interviews about {topic} in {industry}"
                    ]
                }
            }
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "industry": industry,
            "message": "Failed to analyze trends"
        })

