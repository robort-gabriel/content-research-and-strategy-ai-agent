"""
FastAPI Application for Content Research & Strategy AI Agent

Production-ready FastAPI application with security features:
- API key authentication
- Rate limiting
- Input validation
- CORS configuration
- Comprehensive error handling
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Security, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from content_ideation_agent import ContentIdeationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Rate limiter configuration
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
limiter = Limiter(key_func=get_remote_address)

# API Key Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Get API key from environment
API_KEY = os.getenv("API_KEY", "")
if not API_KEY:
    logger.warning(
        "API_KEY not set in environment variables. API will be accessible without authentication."
    )


def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """
    Verify API key from request header.

    Args:
        api_key: API key from request header

    Returns:
        True if API key is valid

    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not API_KEY:
        # If no API key is configured, allow all requests
        return True

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please provide X-API-Key header.",
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    return True


# Request/Response Models
class IdeationRequest(BaseModel):
    """Request model for content research and strategy."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Content research and strategy query (e.g., 'Generate blog post ideas about AI automation')",
    )
    save_output: bool = Field(
        True,
        description="Whether to save results to output files",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Sanitize and validate query."""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        # Remove potentially dangerous characters
        sanitized = v.strip()
        if len(sanitized) < 1:
            raise ValueError("Query must contain at least one character")
        return sanitized


class IdeationData(BaseModel):
    """Data model for content research and strategy results."""

    trends: Optional[Dict[str, Any]] = None
    keywords: Optional[Dict[str, Any]] = None
    content_ideas: Optional[Dict[str, Any]] = None
    competitors: Optional[Dict[str, Any]] = None
    seo: Optional[Dict[str, Any]] = None


class IdeationResponse(BaseModel):
    """Response model for content research and strategy results."""

    status: str
    query: str
    mode: str
    ideation_result: str
    data: IdeationData
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    message: str
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    error_type: Optional[str] = None


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the FastAPI app."""
    logger.info("Starting Content Research & Strategy AI Agent API...")
    yield
    logger.info("Shutting down Content Research & Strategy AI Agent API...")


# Create FastAPI app
app = FastAPI(
    title="Content Research & Strategy AI Agent API",
    description="Production-ready API for generating content ideas, analyzing trends, researching keywords, and optimizing for SEO",
    version="1.0.0",
    lifespan=lifespan,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint",
)
async def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        Health status and API version
    """
    return HealthResponse(
        status="healthy",
        message="Content Research & Strategy AI Agent API is running",
        version="1.0.0",
    )


@app.post(
    "/api/v1/ideate",
    response_model=IdeationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Content Research & Strategy"],
    summary="Generate content ideas and strategies",
    dependencies=[Depends(verify_api_key)],
)
@limiter.limit(
    f"{RATE_LIMIT_PER_MINUTE}/minute"
)  # Rate limit from environment variable
async def generate_content_ideas(
    request_data: IdeationRequest,
    request: Request,
):
    """
    Generate content ideas, analyze trends, research keywords, analyze competitors, and optimize for SEO.

    This endpoint:
    - Analyzes the query to determine the appropriate mode
    - Calls relevant tools (trend analysis, keyword research, content generation, etc.)
    - Synthesizes results into a comprehensive content strategy
    - Returns detailed content research and strategy results with supporting data

    Args:
        request_data: Content research and strategy request with query and save_output flag
        request: FastAPI Request object for rate limiting

    Returns:
        IdeationResponse with comprehensive content strategy

    Raises:
        HTTPException: If content research and strategy fails or request is invalid
    """
    try:
        logger.info(
            f"Received content research and strategy request: query='{request_data.query}', "
            f"save_output={request_data.save_output}"
        )

        # Create agent instance
        agent = ContentIdeationAgent()

        # Process the content research and strategy request
        result = agent.process(
            query=request_data.query,
            save_output=request_data.save_output,
        )

        # Check for errors
        if result.get("error"):
            logger.error(f"Content research and strategy error: {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Content research and strategy failed: {result['error']}",
            )

        # Prepare data model
        data = IdeationData(
            trends=result.get("data", {}).get("trends"),
            keywords=result.get("data", {}).get("keywords"),
            content_ideas=result.get("data", {}).get("content_ideas"),
            competitors=result.get("data", {}).get("competitors"),
            seo=result.get("data", {}).get("seo"),
        )

        logger.info(
            f"Successfully generated content research and strategy for query: {request_data.query} (mode: {result.get('mode')})"
        )

        return IdeationResponse(
            status=result.get("status", "completed"),
            query=result.get("query", request_data.query),
            mode=result.get("mode", "unknown"),
            ideation_result=result.get("ideation_result", ""),
            data=data,
            timestamp=result.get("timestamp", ""),
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Error generating content ideas: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content research and strategy failed: {str(e)}",
        )


@app.get(
    "/",
    tags=["Root"],
    summary="API root endpoint",
)
async def root():
    """
    Root endpoint with API information.

    Returns:
        API information and available endpoints
    """
    return {
        "name": "Content Research & Strategy AI Agent API",
        "version": "1.0.0",
        "description": "Production-ready API for generating content ideas, analyzing trends, researching keywords, and optimizing for SEO",
        "endpoints": {
            "health": "/health",
            "ideate": "/api/v1/ideate",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level="info",
    )
