"""
Content Research & Strategy AI Agent

A LangGraph-powered agent that generates creative content ideas, analyzes trends,
researches keywords, analyzes competitors, and optimizes for SEO.
"""

import os
from datetime import datetime
from typing import TypedDict, Annotated, Sequence, Literal
import operator
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
)
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain.tools import tool

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Import tools
from tools import (
    analyze_trends_tool,
    keyword_research_tool,
    generate_content_ideas_tool,
    analyze_competitor_content_tool,
    optimize_for_seo_tool,
)


# ==================== State Definition ====================


class ContentIdeationState(TypedDict):
    """State for the Content Research & Strategy AI Agent."""

    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    mode: Literal[
        "trend_analysis",
        "keyword_research",
        "idea_generation",
        "competitor_analysis",
        "seo_optimization",
        "comprehensive",
    ]

    # Data fields
    trend_data: dict
    keyword_data: dict
    content_ideas: dict
    competitor_data: dict
    seo_data: dict

    # Final results
    ideation_result: str
    status: str
    error: str | None


# ==================== LLM Service ====================


class LLMService:
    """Service for LLM operations."""

    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=False)

    def determine_mode(self, query: str) -> str:
        """Determine which mode to use based on the query."""
        system_message = """You are a content ideation mode classifier. Analyze the user's query and determine which mode to use:
        
        - trend_analysis: For queries about current trends, trending topics, what's hot
        - keyword_research: For queries about keywords, search terms, SEO keywords
        - idea_generation: For queries about content ideas, what to write about, content suggestions
        - competitor_analysis: For queries about competitor content, content gaps, what competitors are doing
        - seo_optimization: For queries about optimizing content, SEO improvements, meta descriptions
        - comprehensive: For queries that need multiple analyses or full content strategy
        
        Respond with ONLY the mode name, nothing else."""

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Query: {query}"),
        ]

        response = self.model.invoke(messages)
        content = response.content if hasattr(response, "content") else str(response)
        mode = content.strip().lower()

        # Validate mode
        valid_modes = [
            "trend_analysis",
            "keyword_research",
            "idea_generation",
            "competitor_analysis",
            "seo_optimization",
            "comprehensive",
        ]
        if mode not in valid_modes:
            mode = "comprehensive"

        return mode

    def synthesize_ideation(self, query: str, state: ContentIdeationState) -> str:
        """Synthesize all data into a comprehensive content research and strategy response."""
        system_message = """You are an expert content strategist and ideation specialist. 
        Synthesize the provided data into a comprehensive, actionable content strategy.
        
        Create a response that includes:
        1. Executive Summary - Key insights and recommendations
        2. Data Analysis - What the data tells us
        3. Content Opportunities - Specific, actionable content ideas
        4. Implementation Plan - How to execute these ideas
        5. SEO Recommendations - How to optimize for search
        6. Success Metrics - How to measure success
        
        Make your response detailed, practical, and ready to implement."""

        # Gather all available context
        context_parts = []

        if state.get("trend_data"):
            context_parts.append(
                f"TREND ANALYSIS:\n{json.dumps(state['trend_data'], indent=2)}"
            )

        if state.get("keyword_data"):
            context_parts.append(
                f"KEYWORD RESEARCH:\n{json.dumps(state['keyword_data'], indent=2)}"
            )

        if state.get("content_ideas"):
            context_parts.append(
                f"CONTENT IDEAS:\n{json.dumps(state['content_ideas'], indent=2)}"
            )

        if state.get("competitor_data"):
            context_parts.append(
                f"COMPETITOR ANALYSIS:\n{json.dumps(state['competitor_data'], indent=2)}"
            )

        if state.get("seo_data"):
            context_parts.append(
                f"SEO OPTIMIZATION:\n{json.dumps(state['seo_data'], indent=2)}"
            )

        context = "\n\n".join(context_parts) if context_parts else "No data available"

        user_message = f"""Query: {query}
        
Available Data:
{context}

Please provide a comprehensive content ideation strategy based on this data."""

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message),
        ]

        response = self.model.invoke(messages)
        return response.content if hasattr(response, "content") else str(response)


# ==================== Graph Nodes ====================

# Initialize services lazily to allow env loading
_llm_service = None
_llm_with_tools = None


def get_llm_service():
    """Get or create LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_llm_with_tools():
    """Get or create LLM with tools bound."""
    global _llm_with_tools
    if _llm_with_tools is None:
        _llm_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0.7).bind_tools(
            tools
        )
    return _llm_with_tools


# Create tool-calling LLM
tools = [
    analyze_trends_tool,
    keyword_research_tool,
    generate_content_ideas_tool,
    analyze_competitor_content_tool,
    optimize_for_seo_tool,
]


def agent_node(state: ContentIdeationState) -> ContentIdeationState:
    """
    Main agent node that processes the query and decides which tools to call.
    """
    query = state["query"]
    messages = list(state.get("messages", []))
    llm_service = get_llm_service()
    llm_with_tools = get_llm_with_tools()

    # If this is the first run, determine mode and set up the agent
    if not state.get("mode"):
        mode = llm_service.determine_mode(query)
        state["mode"] = mode

        # Create system message based on mode
        system_content = f"""You are a Content Ideation Engine in {mode} mode.
        
Your task: Analyze the user's query and use the appropriate tools to gather insights.

Available tools:
- analyze_trends_tool: Analyze current trends for a topic
- keyword_research_tool: Research keywords and related terms
- generate_content_ideas_tool: Generate creative content ideas
- analyze_competitor_content_tool: Analyze competitor content
- optimize_for_seo_tool: Optimize content for SEO

Query: {query}

Based on the query, call the relevant tools to gather comprehensive insights.
After calling tools, provide a FINAL_ANSWER with your synthesis."""

        messages = [SystemMessage(content=system_content), HumanMessage(content=query)]

    # Call LLM with tools
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    # Check if we have a final answer
    if hasattr(response, "content") and response.content:
        content_lower = response.content.lower()
        if "final_answer" in content_lower or (
            not hasattr(response, "tool_calls") or not response.tool_calls
        ):
            # Extract final answer
            final_answer = response.content
            if "final_answer:" in content_lower:
                final_answer = response.content.split("FINAL_ANSWER:")[-1].strip()
            elif "final_answer" in content_lower:
                final_answer = response.content.split("final_answer")[-1].strip()

            # Synthesize with all available data
            llm_service = get_llm_service()
            synthesized = llm_service.synthesize_ideation(query, state)

            return {
                **state,
                "messages": messages,
                "ideation_result": synthesized,
                "status": "completed",
            }

    return {**state, "messages": messages, "status": "processing"}


def should_continue(state: ContentIdeationState) -> str:
    """Determine whether to continue processing or end."""
    messages = state.get("messages", [])

    if state.get("status") == "completed":
        return "end"

    if not messages:
        return "continue"

    last_message = messages[-1]

    # Check if there are tool calls to execute
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"

    # If no tool calls and we have content, we're done
    if hasattr(last_message, "content") and last_message.content:
        return "end"

    return "continue"


def update_state_with_tool_results(state: ContentIdeationState) -> ContentIdeationState:
    """Update state with tool execution results."""
    messages = list(state.get("messages", []))

    # Find the last ToolMessage
    for message in reversed(messages):
        if isinstance(message, ToolMessage):
            try:
                # Parse the tool result
                result = (
                    json.loads(message.content)
                    if isinstance(message.content, str)
                    else message.content
                )

                # Update state based on tool name
                tool_name = message.name if hasattr(message, "name") else ""

                if "trend" in tool_name.lower():
                    state["trend_data"] = result
                elif "keyword" in tool_name.lower():
                    state["keyword_data"] = result
                elif (
                    "content_ideas" in tool_name.lower()
                    or "generate" in tool_name.lower()
                ):
                    state["content_ideas"] = result
                elif "competitor" in tool_name.lower():
                    state["competitor_data"] = result
                elif "seo" in tool_name.lower():
                    state["seo_data"] = result

            except json.JSONDecodeError:
                # If not JSON, store as is
                pass

    return state


# ==================== Graph Creation ====================


def create_content_ideation_agent():
    """Create and compile the Content Research & Strategy AI Agent graph."""

    # Create the graph
    workflow = StateGraph(ContentIdeationState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("update_state", update_state_with_tool_results)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent", should_continue, {"continue": "tools", "end": END}
    )

    workflow.add_edge("tools", "update_state")
    workflow.add_edge("update_state", "agent")

    # Compile the graph
    return workflow.compile()


# ==================== Agent Interface ====================


class ContentIdeationAgent:
    """Content Research & Strategy AI Agent Interface."""

    def __init__(self):
        self.graph = create_content_ideation_agent()
        self.log_entries = []

    def _log(self, message: str, data: dict = None):
        """Log agent activity."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "data": data,
        }
        self.log_entries.append(entry)
        print(f"[{entry['timestamp']}] {message}")
        if data:
            print(f"  Data: {json.dumps(data, indent=2)[:200]}...")

    def process(self, query: str, save_output: bool = True) -> dict:
        """
        Process a content research and strategy query.

        Args:
            query: The content research and strategy query
            save_output: Whether to save results to file

        Returns:
            Dictionary with research and strategy results and metadata
        """
        self._log(f"Processing query: {query}")

        # Initialize state
        initial_state = {
            "messages": [],
            "query": query,
            "mode": "",
            "trend_data": {},
            "keyword_data": {},
            "content_ideas": {},
            "competitor_data": {},
            "seo_data": {},
            "ideation_result": "",
            "status": "initialized",
            "error": None,
        }

        try:
            # Run the graph
            self._log("Running LangGraph workflow...")
            final_state = self.graph.invoke(initial_state)

            self._log(
                "Workflow completed",
                {"mode": final_state.get("mode"), "status": final_state.get("status")},
            )

            # Prepare result
            result = {
                "query": query,
                "mode": final_state.get("mode", "unknown"),
                "ideation_result": final_state.get("ideation_result", ""),
                "data": {
                    "trends": final_state.get("trend_data", {}),
                    "keywords": final_state.get("keyword_data", {}),
                    "content_ideas": final_state.get("content_ideas", {}),
                    "competitors": final_state.get("competitor_data", {}),
                    "seo": final_state.get("seo_data", {}),
                },
                "timestamp": datetime.now().isoformat(),
                "status": final_state.get("status", "unknown"),
            }

            # Save to file if requested
            if save_output:
                self._save_output(result)
                self._save_log()

            return result

        except Exception as e:
            self._log(f"Error during processing: {str(e)}")
            return {
                "query": query,
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
            }

    def _save_output(self, result: dict):
        """Save ideation results to markdown file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create safe filename from query
        safe_query = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "_" for c in result["query"]
        )
        safe_query = safe_query[:50]  # Limit length

        filename = f"output/content_research_strategy_{safe_query}_{timestamp}.md"

        with open(filename, "w") as f:
            f.write(f"# Content Research & Strategy Results\n\n")
            f.write(f"**Query:** {result['query']}\n\n")
            f.write(f"**Mode:** {result['mode']}\n\n")
            f.write(f"**Generated:** {result['timestamp']}\n\n")
            f.write(f"---\n\n")
            f.write(f"## Content Strategy\n\n")
            f.write(result.get("ideation_result", "No results generated"))
            f.write(f"\n\n---\n\n")
            f.write(f"## Supporting Data\n\n")

            if result["data"].get("trends"):
                f.write(f"### Trend Analysis\n\n")
                f.write(
                    f"```json\n{json.dumps(result['data']['trends'], indent=2)}\n```\n\n"
                )

            if result["data"].get("keywords"):
                f.write(f"### Keyword Research\n\n")
                f.write(
                    f"```json\n{json.dumps(result['data']['keywords'], indent=2)}\n```\n\n"
                )

            if result["data"].get("content_ideas"):
                f.write(f"### Content Ideas\n\n")
                f.write(
                    f"```json\n{json.dumps(result['data']['content_ideas'], indent=2)}\n```\n\n"
                )

            if result["data"].get("competitors"):
                f.write(f"### Competitor Analysis\n\n")
                f.write(
                    f"```json\n{json.dumps(result['data']['competitors'], indent=2)}\n```\n\n"
                )

            if result["data"].get("seo"):
                f.write(f"### SEO Optimization\n\n")
                f.write(
                    f"```json\n{json.dumps(result['data']['seo'], indent=2)}\n```\n\n"
                )

        self._log(f"Results saved to {filename}")

    def _save_log(self):
        """Save agent log to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"output/content_research_strategy_log_{timestamp}.txt"

        with open(log_filename, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("CONTENT RESEARCH & STRATEGY AI AGENT - EXECUTION LOG\n")
            f.write("=" * 80 + "\n\n")

            for entry in self.log_entries:
                f.write(f"[{entry['timestamp']}] {entry['message']}\n")
                if entry.get("data"):
                    f.write(f"{json.dumps(entry['data'], indent=2)}\n")
                f.write("-" * 80 + "\n")

        self._log(f"Log saved to {log_filename}")
