"""SEO optimization tool for content ideas."""

from langchain.tools import tool
import json
from datetime import datetime
from typing import Dict, Any, List


@tool
def optimize_for_seo_tool(content_title: str, target_keyword: str, content_outline: str = "") -> str:
    """
    Optimize content for SEO with title suggestions, meta descriptions, and structure recommendations.
    
    Args:
        content_title: The proposed content title
        target_keyword: Primary keyword to optimize for
        content_outline: Optional content outline or summary
    
    Returns:
        JSON string with SEO-optimized suggestions, title variations, and structure recommendations
    """
    try:
        # Generate optimized title variations
        title_variations = _generate_seo_titles(content_title, target_keyword)
        
        # Generate meta description
        meta_description = _generate_meta_description(content_title, target_keyword, content_outline)
        
        # Generate URL slug
        url_slug = _generate_url_slug(content_title, target_keyword)
        
        # Content structure recommendations
        structure_recommendations = _generate_structure_recommendations(target_keyword)
        
        # Generate header suggestions
        headers = _generate_header_suggestions(target_keyword, content_outline)
        
        # Internal linking suggestions
        internal_links = _generate_internal_link_suggestions(target_keyword)
        
        result = {
            "original_title": content_title,
            "target_keyword": target_keyword,
            "optimized_at": datetime.now().isoformat(),
            "seo_optimization": {
                "title_variations": title_variations,
                "recommended_title": title_variations[0] if title_variations else content_title,
                "title_tips": [
                    "Keep under 60 characters for full display in search results",
                    "Include primary keyword near the beginning",
                    "Add numbers or power words to increase CTR",
                    "Make it compelling and unique"
                ]
            },
            "meta_data": {
                "meta_description": meta_description,
                "meta_description_tips": [
                    "Keep between 150-160 characters",
                    "Include primary keyword naturally",
                    "Add a clear call-to-action",
                    "Make it unique for each page"
                ],
                "url_slug": url_slug,
                "url_tips": [
                    "Use hyphens to separate words",
                    "Keep it short and descriptive",
                    "Include primary keyword",
                    "Avoid stop words when possible"
                ]
            },
            "content_structure": {
                "recommended_length": "1500-2500 words for comprehensive topics",
                "header_hierarchy": headers,
                "structure_tips": structure_recommendations,
                "keyword_placement": {
                    "title": "Include primary keyword",
                    "h1": "Use primary keyword naturally",
                    "h2_h3": "Use variations and related keywords",
                    "first_paragraph": "Include primary keyword within first 100 words",
                    "throughout_content": "Maintain 1-2% keyword density",
                    "conclusion": "Repeat primary keyword naturally"
                }
            },
            "on_page_seo": {
                "image_optimization": [
                    "Use descriptive file names with keywords",
                    "Add alt text to all images",
                    "Compress images for fast loading",
                    "Use responsive images"
                ],
                "internal_linking": internal_links,
                "external_linking": [
                    "Link to 2-3 authoritative sources",
                    "Use descriptive anchor text",
                    "Link to relevant, high-quality sites",
                    "Open external links in new tab"
                ],
                "schema_markup": [
                    "Add Article schema",
                    "Include FAQ schema if applicable",
                    "Add HowTo schema for tutorials",
                    "Use Breadcrumb schema for navigation"
                ]
            },
            "technical_seo": {
                "page_speed": [
                    "Aim for under 3 seconds load time",
                    "Optimize images and videos",
                    "Minify CSS and JavaScript",
                    "Use browser caching"
                ],
                "mobile_optimization": [
                    "Ensure responsive design",
                    "Use readable font sizes (16px+)",
                    "Avoid intrusive interstitials",
                    "Make buttons easy to tap"
                ],
                "core_web_vitals": [
                    "LCP (Largest Contentful Paint): < 2.5s",
                    "FID (First Input Delay): < 100ms",
                    "CLS (Cumulative Layout Shift): < 0.1"
                ]
            },
            "content_tips": [
                "Write for humans first, search engines second",
                "Use short paragraphs (2-3 sentences max)",
                "Include bullet points and lists for readability",
                "Add relevant images, videos, or infographics",
                "Update content regularly to maintain freshness",
                "Encourage engagement (comments, shares)",
                "Monitor performance and iterate"
            ]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "content_title": content_title,
            "target_keyword": target_keyword,
            "message": "Failed to generate SEO optimization"
        })


def _generate_seo_titles(title: str, keyword: str) -> List[str]:
    """Generate SEO-optimized title variations."""
    variations = []
    
    # Current year for freshness
    current_year = datetime.now().year
    
    # If keyword not in title, create variations that include it
    if keyword.lower() not in title.lower():
        variations.append(f"{keyword}: {title}")
        variations.append(f"{title} - {keyword} Guide")
    
    # Add power words and numbers
    power_variations = [
        f"Complete Guide to {keyword} | {title}",
        f"{keyword}: {title} [{current_year}]",
        f"How to Master {keyword} - {title}",
        f"{title} | {keyword} Best Practices",
        f"Ultimate {keyword} Guide: {title}"
    ]
    
    variations.extend(power_variations)
    
    # Ensure all titles are under 60 characters when possible
    optimized = []
    for var in variations:
        if len(var) <= 60:
            optimized.append(var)
        else:
            # Truncate smartly
            optimized.append(var[:57] + "...")
    
    return optimized[:5]


def _generate_meta_description(title: str, keyword: str, outline: str) -> str:
    """Generate SEO-optimized meta description."""
    base = f"Learn about {keyword} in this comprehensive guide. "
    
    if outline:
        # Extract key points from outline
        base += f"Discover {title.lower()} including best practices, tips, and strategies. "
    else:
        base += f"Everything you need to know about {keyword} including expert tips and actionable insights. "
    
    cta = "Read more!"
    
    description = base + cta
    
    # Ensure it's within optimal length
    if len(description) > 160:
        description = description[:157] + "..."
    elif len(description) < 120:
        description = base + f"Get started with {keyword} today. " + cta
    
    return description


def _generate_url_slug(title: str, keyword: str) -> str:
    """Generate SEO-friendly URL slug."""
    import re
    
    # Combine title and keyword
    text = f"{title} {keyword}".lower()
    
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', text)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    
    # Remove stop words for cleaner URL
    stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are'}
    words = slug.split('-')
    filtered_words = [w for w in words if w not in stop_words]
    
    slug = '-'.join(filtered_words[:8])  # Limit to 8 words
    
    return slug.strip('-')


def _generate_structure_recommendations(keyword: str) -> List[str]:
    """Generate content structure recommendations."""
    return [
        "Start with a compelling introduction that includes the primary keyword",
        "Use H1 for main title, H2 for major sections, H3 for subsections",
        f"Include '{keyword}' in at least 2-3 H2 headings naturally",
        "Add table of contents for long-form content (1500+ words)",
        "Break content into scannable sections with clear headings",
        "Include bullet points and numbered lists for easy reading",
        "Add relevant images or videos every 300-500 words",
        "Use bold and italic sparingly to emphasize key points",
        "Include a summary or key takeaways section",
        "End with a strong call-to-action"
    ]


def _generate_header_suggestions(keyword: str, outline: str) -> Dict[str, List[str]]:
    """Generate header hierarchy suggestions."""
    return {
        "H1": f"Main title with {keyword} (use only once)",
        "H2_suggestions": [
            f"What is {keyword}?",
            f"Why {keyword} Matters",
            f"How to Use {keyword}",
            f"Best Practices for {keyword}",
            f"{keyword} Tips and Strategies",
            f"Common {keyword} Mistakes to Avoid",
            f"Conclusion"
        ],
        "H3_suggestions": [
            "Use H3s to break down H2 sections into subtopics",
            "Include variations of the primary keyword",
            "Use question-based H3s for featured snippet optimization",
            f"Example H3s: 'Getting Started with {keyword}', 'Advanced {keyword} Techniques'"
        ]
    }


def _generate_internal_link_suggestions(keyword: str) -> List[str]:
    """Generate internal linking suggestions."""
    return [
        f"Link to related '{keyword}' articles or guides",
        "Add 3-5 contextual internal links to relevant pages",
        "Use descriptive anchor text (not 'click here')",
        f"Link to cornerstone content about {keyword}",
        "Consider adding a 'Related Articles' section at the end",
        "Link to category or topic pages",
        f"Add links from high-authority pages to this new {keyword} content"
    ]

