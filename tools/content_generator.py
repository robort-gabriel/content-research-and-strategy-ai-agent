"""Content idea generation tool."""

from langchain.tools import tool
import json
from datetime import datetime
from typing import List, Dict, Any


@tool
def generate_content_ideas_tool(topic: str, content_type: str = "blog", target_audience: str = "general", count: int = 5) -> str:
    """
    Generate creative content ideas based on a topic.
    
    Args:
        topic: The main topic for content ideas
        content_type: Type of content (blog, video, social, newsletter, ebook)
        target_audience: Target audience description
        count: Number of ideas to generate (default: 5)
    
    Returns:
        JSON string with creative content ideas, titles, and outlines
    """
    try:
        # Content format templates
        formats = {
            "blog": [
                "How-to Guide",
                "Listicle",
                "Case Study",
                "Expert Interview",
                "Comparison Post",
                "Ultimate Guide",
                "Myth Busting",
                "Trend Analysis"
            ],
            "video": [
                "Tutorial",
                "Behind-the-Scenes",
                "Product Demo",
                "Expert Q&A",
                "Animated Explainer",
                "Customer Story",
                "Quick Tips"
            ],
            "social": [
                "Infographic",
                "Carousel Post",
                "Poll/Survey",
                "Quote Graphics",
                "Before/After",
                "User-Generated Content",
                "Mini-Tutorial"
            ],
            "newsletter": [
                "Weekly Roundup",
                "Industry Insights",
                "Exclusive Tips",
                "Community Spotlight",
                "Product Updates",
                "Resource Library"
            ],
            "ebook": [
                "Comprehensive Guide",
                "Best Practices Handbook",
                "Industry Report",
                "Step-by-Step Playbook",
                "Research Findings"
            ]
        }
        
        selected_formats = formats.get(content_type.lower(), formats["blog"])
        
        # Generate ideas
        ideas = []
        for i in range(min(count, 10)):
            format_type = selected_formats[i % len(selected_formats)]
            
            if content_type == "blog":
                idea = _generate_blog_idea(topic, format_type, target_audience, i)
            elif content_type == "video":
                idea = _generate_video_idea(topic, format_type, target_audience, i)
            elif content_type == "social":
                idea = _generate_social_idea(topic, format_type, target_audience, i)
            elif content_type == "newsletter":
                idea = _generate_newsletter_idea(topic, format_type, target_audience, i)
            elif content_type == "ebook":
                idea = _generate_ebook_idea(topic, format_type, target_audience, i)
            else:
                idea = _generate_generic_idea(topic, format_type, target_audience, i)
            
            ideas.append(idea)
        
        result = {
            "topic": topic,
            "content_type": content_type,
            "target_audience": target_audience,
            "generated_at": datetime.now().isoformat(),
            "ideas_count": len(ideas),
            "content_ideas": ideas,
            "implementation_tips": [
                "Validate ideas with your target audience before full production",
                "Create a content calendar to schedule these ideas",
                "Repurpose successful content across multiple formats",
                "Track engagement metrics to refine future ideation",
                "Collaborate with subject matter experts for authenticity"
            ]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to generate content ideas"
        })


def _generate_blog_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate a blog post idea."""
    titles = [
        f"The Ultimate Guide to {topic} for {audience}",
        f"10 {topic} Strategies That Actually Work in 2025",
        f"How to Master {topic}: A Step-by-Step Guide",
        f"{topic} vs. Alternatives: Which Is Right for You?",
        f"7 Common {topic} Mistakes (And How to Avoid Them)",
        f"Case Study: How We Used {topic} to Achieve Results",
        f"The Future of {topic}: Trends to Watch",
        f"Beginner's Guide to {topic}: Everything You Need to Know"
    ]
    
    return {
        "id": f"blog_{index + 1}",
        "format": format_type,
        "title": titles[index % len(titles)],
        "description": f"A comprehensive {format_type.lower()} about {topic} tailored for {audience}",
        "outline": [
            "Introduction - Hook and problem statement",
            "Background - Context and importance",
            "Main Content - Core insights and strategies",
            "Examples/Case Studies - Real-world applications",
            "Action Steps - Practical implementation guide",
            "Conclusion - Key takeaways and CTA"
        ],
        "estimated_length": "1500-2000 words",
        "keywords": [topic, f"{topic} guide", f"{topic} tips", audience],
        "cta": f"Download our free {topic} checklist"
    }


def _generate_video_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate a video content idea."""
    titles = [
        f"{topic} Tutorial: Complete Walkthrough",
        f"5-Minute {topic} Tips for Busy {audience}",
        f"Behind the Scenes: How We Use {topic}",
        f"{topic} Demo: Real-Time Implementation",
        f"Expert Interview: Mastering {topic}",
        f"Customer Success Story: {topic} in Action"
    ]
    
    return {
        "id": f"video_{index + 1}",
        "format": format_type,
        "title": titles[index % len(titles)],
        "description": f"Engaging video content about {topic} for {audience}",
        "script_outline": [
            "Hook (0-10s) - Grab attention",
            "Problem Statement (10-30s) - What pain point",
            "Solution Introduction (30s-1m) - Present {topic}",
            "Demonstration (1m-3m) - Show how it works",
            "Results (3m-4m) - Benefits and outcomes",
            "CTA (4m-5m) - Next steps"
        ],
        "estimated_length": "3-5 minutes",
        "production_notes": "Screen recording + talking head or animation",
        "thumbnail_idea": f"Bold text: '{topic}' + visual metaphor",
        "platform": "YouTube, LinkedIn, Instagram Reels"
    }


def _generate_social_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate a social media content idea."""
    return {
        "id": f"social_{index + 1}",
        "format": format_type,
        "title": f"{topic} Quick Tip #{index + 1}",
        "description": f"Engaging social post about {topic}",
        "content_structure": [
            f"Slide 1: Eye-catching title about {topic}",
            f"Slide 2-3: Key insights about {topic}",
            f"Slide 4: Action step for {audience}",
            f"Slide 5: CTA and engagement prompt"
        ],
        "copy_example": f"🚀 Master {topic} in 5 simple steps! Swipe for actionable tips → [Carousel content] What's your biggest {topic} challenge? Comment below! 💬",
        "hashtags": [f"#{topic.replace(' ', '')}", "#Tips", "#HowTo", f"#{audience.replace(' ', '')}"],
        "best_posting_time": "Tuesday-Thursday, 10am-2pm",
        "platforms": ["Instagram", "LinkedIn", "Twitter"]
    }


def _generate_newsletter_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate a newsletter content idea."""
    return {
        "id": f"newsletter_{index + 1}",
        "format": format_type,
        "subject_line": f"Your weekly {topic} insights + exclusive tips",
        "description": f"Curated newsletter content about {topic}",
        "sections": [
            f"📰 This Week in {topic}",
            f"💡 Expert Tip: Advanced {topic} strategy",
            f"📊 Stat of the Week: {topic} trends",
            f"🔧 Tool Spotlight: Best {topic} resources",
            f"👥 Community Highlight: Reader success story",
            f"📚 Recommended Reading: {topic} articles"
        ],
        "word_count": "500-800 words",
        "send_frequency": "Weekly",
        "cta": f"Try our {topic} tool free for 14 days"
    }


def _generate_ebook_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate an ebook content idea."""
    return {
        "id": f"ebook_{index + 1}",
        "format": format_type,
        "title": f"The Complete {topic} Playbook for {audience}",
        "description": f"Comprehensive ebook about {topic}",
        "chapters": [
            f"Chapter 1: Introduction to {topic}",
            f"Chapter 2: Core Concepts and Fundamentals",
            f"Chapter 3: Advanced {topic} Strategies",
            f"Chapter 4: Real-World Case Studies",
            f"Chapter 5: Common Challenges and Solutions",
            f"Chapter 6: Tools and Resources",
            f"Chapter 7: Implementation Roadmap",
            f"Chapter 8: Measuring Success"
        ],
        "page_count": "30-50 pages",
        "design_elements": "Infographics, charts, worksheets, checklists",
        "lead_magnet": True,
        "distribution": "Gated content on website + email nurture sequence"
    }


def _generate_generic_idea(topic: str, format_type: str, audience: str, index: int) -> Dict[str, Any]:
    """Generate a generic content idea."""
    return {
        "id": f"content_{index + 1}",
        "format": format_type,
        "title": f"{format_type}: {topic} for {audience}",
        "description": f"Content about {topic} targeting {audience}",
        "outline": [
            "Introduction",
            "Main points",
            "Supporting details",
            "Conclusion and CTA"
        ]
    }

