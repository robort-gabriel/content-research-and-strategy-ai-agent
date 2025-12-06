"""Competitor content analysis tool."""

from langchain.tools import tool
from tavily import TavilyClient
import os
import json
from datetime import datetime
from typing import Dict, Any, List
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
def analyze_competitor_content_tool(topic: str, competitors: str = "", top_n: int = 5) -> str:
    """
    Analyze competitor content for a given topic to identify gaps and opportunities.
    
    Args:
        topic: The topic to analyze competitor content for
        competitors: Comma-separated list of competitor domains (optional)
        top_n: Number of top-performing content pieces to analyze
    
    Returns:
        JSON string with competitor analysis, content gaps, and differentiation opportunities
    """
    try:
        client = _get_tavily_client()
        competitor_list = [c.strip() for c in competitors.split(",")] if competitors else []
        
        if client:
            # Search for content on the topic
            query = f"{topic} guide tutorial best practices"
            results = client.search(
                query=query,
                max_results=15,
                search_depth="advanced"
            )
            
            # Analyze competitor content
            competitor_content = []
            content_types = {
                "guide": 0,
                "tutorial": 0,
                "listicle": 0,
                "case_study": 0,
                "video": 0,
                "infographic": 0,
                "other": 0
            }
            
            for result in results.get("results", [])[:top_n]:
                title = result.get("title", "").lower()
                content = result.get("content", "")
                url = result.get("url", "")
                
                # Classify content type
                if "how to" in title or "guide" in title:
                    ctype = "guide"
                elif "tutorial" in title or "step by step" in title:
                    ctype = "tutorial"
                elif any(str(i) in title for i in range(1, 20)):
                    ctype = "listicle"
                elif "case study" in title or "success story" in title:
                    ctype = "case_study"
                elif "video" in title or "watch" in title:
                    ctype = "video"
                else:
                    ctype = "other"
                
                content_types[ctype] += 1
                
                competitor_content.append({
                    "title": result.get("title", ""),
                    "url": url,
                    "content_type": ctype,
                    "snippet": content[:200],
                    "score": result.get("score", 0),
                    "estimated_length": len(content),
                    "is_competitor": any(comp in url for comp in competitor_list) if competitor_list else False
                })
            
            # Identify gaps
            underrepresented_formats = [k for k, v in content_types.items() if v < 2 and k != "other"]
            
            analysis = {
                "topic": topic,
                "analyzed_at": datetime.now().isoformat(),
                "competitors_analyzed": len(competitor_content),
                "competitor_domains": competitor_list if competitor_list else "Auto-detected top performers",
                "top_performing_content": competitor_content,
                "content_type_distribution": content_types,
                "insights": {
                    "dominant_formats": [k for k, v in sorted(content_types.items(), key=lambda x: x[1], reverse=True)[:3]],
                    "underrepresented_formats": underrepresented_formats,
                    "average_content_length": sum(c["estimated_length"] for c in competitor_content) // len(competitor_content) if competitor_content else 0,
                    "high_performing_patterns": _identify_patterns(competitor_content)
                },
                "content_gaps": _identify_content_gaps(topic, content_types, competitor_content),
                "differentiation_opportunities": [
                    "Create more comprehensive content than competitors",
                    f"Focus on underrepresented formats: {', '.join(underrepresented_formats) if underrepresented_formats else 'All formats covered'}",
                    "Add unique data, research, or expert insights",
                    "Target long-tail keywords competitors missed",
                    "Improve visual design and user experience",
                    "Update outdated competitor content with fresh insights"
                ]
            }
        else:
            # Fallback analysis
            analysis = {
                "topic": topic,
                "analyzed_at": datetime.now().isoformat(),
                "note": "Using fallback mode - install Tavily for real competitor analysis",
                "mock_insights": {
                    "dominant_formats": ["guide", "tutorial", "listicle"],
                    "content_gaps": [
                        f"Beginner-friendly {topic} tutorials",
                        f"Advanced {topic} strategies",
                        f"Video content about {topic}",
                        f"Interactive {topic} tools",
                        f"Case studies featuring {topic}"
                    ],
                    "differentiation_opportunities": [
                        "Create more comprehensive content than competitors",
                        "Add unique data, research, or expert insights",
                        "Target long-tail keywords competitors missed",
                        "Focus on specific audience segments",
                        "Provide free tools or templates"
                    ]
                }
            }
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to analyze competitor content"
        })


def _identify_patterns(content_list: List[Dict[str, Any]]) -> List[str]:
    """Identify patterns in high-performing content."""
    patterns = []
    
    # Analyze titles
    titles = [c["title"].lower() for c in content_list if c.get("score", 0) > 0.7]
    
    if any("ultimate" in t or "complete" in t for t in titles):
        patterns.append("Comprehensive, authoritative titles perform well")
    
    if any(str(i) in t for t in titles for i in range(1, 20)):
        patterns.append("Numbered lists attract attention")
    
    if any("2024" in t or "2025" in t for t in titles):
        patterns.append("Current year in titles signals freshness")
    
    if any("beginner" in t or "guide" in t for t in titles):
        patterns.append("Beginner-focused content has strong appeal")
    
    return patterns if patterns else ["No clear patterns identified"]


def _identify_content_gaps(topic: str, content_types: Dict[str, int], content_list: List[Dict[str, Any]]) -> List[str]:
    """Identify content gaps and opportunities."""
    gaps = []
    
    # Format gaps
    if content_types.get("video", 0) == 0:
        gaps.append(f"No video content found - opportunity for video tutorial on {topic}")
    
    if content_types.get("case_study", 0) < 2:
        gaps.append(f"Limited case studies - opportunity to showcase real-world {topic} examples")
    
    if content_types.get("infographic", 0) == 0:
        gaps.append(f"No visual content - opportunity for {topic} infographic or visual guide")
    
    # Check for beginner vs advanced content
    beginner_count = sum(1 for c in content_list if "beginner" in c["title"].lower())
    advanced_count = sum(1 for c in content_list if "advanced" in c["title"].lower())
    
    if beginner_count < 2:
        gaps.append(f"Limited beginner content - create introductory {topic} guide")
    
    if advanced_count < 2:
        gaps.append(f"Limited advanced content - develop expert-level {topic} strategies")
    
    # Check for comparison content
    comparison_count = sum(1 for c in content_list if "vs" in c["title"].lower() or "compare" in c["title"].lower())
    if comparison_count == 0:
        gaps.append(f"No comparison content - opportunity for '{topic} vs alternatives' article")
    
    return gaps if gaps else [f"Market is saturated - focus on unique angles or niche aspects of {topic}"]

