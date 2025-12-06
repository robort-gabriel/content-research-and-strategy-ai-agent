"""Keyword research tool for identifying content opportunities."""

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
def keyword_research_tool(primary_keyword: str, context: str = "") -> str:
    """
    Research keywords and related terms for content creation.
    
    Args:
        primary_keyword: The main keyword to research
        context: Additional context about the content topic
    
    Returns:
        JSON string with keyword suggestions, related terms, and search insights
    """
    try:
        client = _get_tavily_client()
        
        if client:
            # Search for content related to the keyword
            query = f"{primary_keyword} {context} guide tutorial how-to"
            results = client.search(
                query=query,
                max_results=8,
                search_depth="basic"
            )
            
            # Extract related keywords from titles and content
            related_keywords = set()
            content_angles = []
            
            for result in results.get("results", []):
                title = result.get("title", "").lower()
                content = result.get("content", "").lower()
                
                # Simple keyword extraction (in production, use NLP)
                words = (title + " " + content).split()
                for word in words:
                    if len(word) > 4 and word.isalpha():
                        related_keywords.add(word)
                
                content_angles.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", "")
                })
            
            research = {
                "primary_keyword": primary_keyword,
                "context": context,
                "researched_at": datetime.now().isoformat(),
                "keyword_suggestions": {
                    "long_tail_keywords": [
                        f"how to use {primary_keyword}",
                        f"best {primary_keyword} for beginners",
                        f"{primary_keyword} vs alternatives",
                        f"{primary_keyword} tips and tricks",
                        f"{primary_keyword} case study"
                    ],
                    "related_terms": list(related_keywords)[:15],
                    "question_keywords": [
                        f"what is {primary_keyword}",
                        f"why use {primary_keyword}",
                        f"when to use {primary_keyword}",
                        f"how does {primary_keyword} work"
                    ]
                },
                "content_angles": content_angles[:5],
                "seo_recommendations": {
                    "title_length": "50-60 characters",
                    "meta_description": "150-160 characters",
                    "keyword_density": "1-2%",
                    "content_length": "1500-2500 words for comprehensive guides"
                }
            }
        else:
            # Fallback: Basic keyword suggestions
            research = {
                "primary_keyword": primary_keyword,
                "context": context,
                "researched_at": datetime.now().isoformat(),
                "keyword_suggestions": {
                    "long_tail_keywords": [
                        f"how to use {primary_keyword}",
                        f"best {primary_keyword} for beginners",
                        f"{primary_keyword} vs alternatives",
                        f"{primary_keyword} guide 2025",
                        f"{primary_keyword} tutorial"
                    ],
                    "related_terms": [
                        f"{primary_keyword} tools",
                        f"{primary_keyword} software",
                        f"{primary_keyword} platform",
                        f"{primary_keyword} service",
                        f"{primary_keyword} solution"
                    ],
                    "question_keywords": [
                        f"what is {primary_keyword}",
                        f"why use {primary_keyword}",
                        f"when to use {primary_keyword}",
                        f"how does {primary_keyword} work",
                        f"who needs {primary_keyword}"
                    ]
                },
                "note": "Using fallback mode - install Tavily for enhanced keyword research",
                "seo_recommendations": {
                    "title_length": "50-60 characters",
                    "meta_description": "150-160 characters",
                    "keyword_density": "1-2%",
                    "content_length": "1500-2500 words for comprehensive guides"
                }
            }
        
        return json.dumps(research, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "primary_keyword": primary_keyword,
            "message": "Failed to research keywords"
        })

