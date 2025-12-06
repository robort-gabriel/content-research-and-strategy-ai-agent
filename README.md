# Content Research & Strategy AI Agent 🚀

A production-ready FastAPI application powered by LangGraph that generates creative content ideas, analyzes trends, researches keywords, analyzes competitors, and optimizes content for SEO.

## 🌟 Features

### 1. **Trend Analysis**
- Discover trending topics in any industry
- Real-time trend data using Tavily API
- Content opportunity identification
- Relevance scoring and insights

### 2. **Keyword Research**
- Comprehensive keyword suggestions
- Long-tail keyword generation
- Related terms discovery
- Question-based keyword opportunities
- SEO recommendations

### 3. **Content Idea Generation**
- Generate creative content ideas for multiple formats:
  - Blog posts & articles
  - Video content
  - Social media posts
  - Newsletters
  - eBooks & guides
- Customizable by target audience
- Complete outlines and structures
- Implementation tips

### 4. **Competitor Analysis**
- Analyze competitor content strategies
- Identify content gaps and opportunities
- Format distribution analysis
- High-performing content patterns
- Differentiation strategies

### 5. **SEO Optimization**
- SEO-optimized title variations
- Meta description generation
- URL slug optimization
- Content structure recommendations
- Header hierarchy suggestions
- Internal/external linking strategies
- Technical SEO checklist

### 6. **Comprehensive Mode**
- Combines all analyses for full content strategy
- Actionable implementation plans
- Success metrics and KPIs
- Executive summaries

## 🔐 Security Features

- **API Key Authentication** - Secure header-based authentication
- **Rate Limiting** - Configurable per-minute rate limits
- **Input Validation** - Pydantic models for request validation
- **CORS Support** - Configurable cross-origin resource sharing
- **Error Handling** - Comprehensive error handling with proper HTTP status codes

## 🏗️ Architecture

Built using **LangGraph** and **FastAPI** with:
- **State Management**: TypedDict-based state tracking
- **Tool Integration**: 5 specialized tools for content research and strategy
- **LLM Orchestration**: GPT-4o-mini for intelligent routing
- **Conditional Routing**: Dynamic workflow based on query intent
- **Comprehensive Logging**: Detailed execution logs for transparency
- **RESTful API**: Production-ready FastAPI endpoints

### Workflow

```
User Query → Mode Detection → Tool Selection → Data Gathering → Synthesis → API Response
```

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key (required)
- Tavily API key (optional, has fallback mode)
- API key for authentication (optional, set `API_KEY` in `.env`)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd content_research_strategy_agent
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Security
API_KEY=your_api_key_for_authentication
RATE_LIMIT_PER_MINUTE=10

# Optional - Server Configuration
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=*
DEBUG=False

# Optional - Enhanced Features
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Start the API Server

```bash
./start_api.sh
```

Or manually:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Generate Content Ideas

```bash
curl -X POST "http://localhost:8000/api/v1/ideate" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate blog post ideas about AI automation for small businesses",
    "save_output": true
  }'
```

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example Queries

**1. Content Idea Generation:**
```json
{
  "query": "Generate 5 video content ideas about sustainable living for millennials"
}
```

**2. Trend Analysis:**
```json
{
  "query": "What are the trending topics in artificial intelligence?"
}
```

**3. Keyword Research:**
```json
{
  "query": "Research keywords for 'electric vehicle charging stations'"
}
```

**4. Competitor Analysis:**
```json
{
  "query": "Analyze competitor content for 'remote work productivity tools'"
}
```

**5. SEO Optimization:**
```json
{
  "query": "Optimize my blog post title: 'How to Learn Python' for keyword 'Python tutorial'"
}
```

**6. Comprehensive Strategy:**
```json
{
  "query": "Create a complete content strategy for launching a new SaaS product for developers"
}
```

For detailed API documentation, see [API_USAGE.md](API_USAGE.md).

## 🛠️ Available Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `analyze_trends_tool` | Analyze current trends | topic, industry | Trending topics with insights |
| `keyword_research_tool` | Research keywords | primary_keyword, context | Keyword suggestions, related terms |
| `generate_content_ideas_tool` | Generate content ideas | topic, content_type, audience | Creative content ideas with outlines |
| `analyze_competitor_content_tool` | Analyze competitors | topic, competitors | Competitor analysis, content gaps |
| `optimize_for_seo_tool` | SEO optimization | title, keyword, outline | SEO recommendations, optimized titles |

## 🔄 Modes

The agent automatically detects and operates in different modes:

- **trend_analysis**: For trend-related queries
- **keyword_research**: For keyword and SEO research
- **idea_generation**: For content idea generation
- **competitor_analysis**: For competitive analysis
- **seo_optimization**: For SEO optimization
- **comprehensive**: For multi-faceted content strategy

## 📊 Output

The API generates two types of output files in the `output/` directory (when `save_output=true`):

### 1. **Content Research & Strategy Results** (`.md` file)
- Query and mode information
- Comprehensive content strategy
- Supporting data from all tools
- Structured in markdown format

### 2. **Execution Log** (`.txt` file)
- Timestamp-based activity log
- Tool execution details
- State transitions
- Debug information

## 🎯 Use Cases

1. **Content Marketers**: Generate blog post ideas and content calendars
2. **SEO Specialists**: Research keywords and optimize content
3. **Social Media Managers**: Create engaging social content ideas
4. **Product Marketers**: Analyze competitor strategies
5. **Agency Teams**: Develop comprehensive content strategies
6. **Bloggers**: Discover trending topics and optimize posts
7. **Video Creators**: Generate video content ideas and scripts

## 📈 Best Practices

1. **Be Specific**: More specific queries yield better results
   - ❌ "content ideas"
   - ✅ "blog post ideas about AI automation for small business owners"

2. **Include Context**: Provide target audience and industry
   - ❌ "trending topics"
   - ✅ "trending topics in sustainable technology for Gen Z"

3. **Use Comprehensive Mode**: For full content strategies, use comprehensive queries

4. **Validate Results**: Always validate AI-generated ideas with your domain expertise

5. **Monitor Logs**: Review execution logs in `output/` directory for debugging

## 🔧 Configuration

### Rate Limiting

Adjust rate limits in `.env`:

```env
RATE_LIMIT_PER_MINUTE=10  # Requests per minute per IP
```

### CORS Configuration

Configure allowed origins:

```env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### API Key Authentication

Set `API_KEY` in `.env` to enable authentication. If not set, API is accessible without authentication (not recommended for production).

### LLM Model

To change the LLM model, edit `content_ideation_agent.py`:

```python
self.model = ChatOpenAI(
    model="gpt-4o",  # or "gpt-4-turbo", "gpt-4"
    temperature=0.7,
    streaming=False
)
```

## 🐛 Troubleshooting

### Issue: API Key Not Working

**Solution:**
1. Check that `API_KEY` is set in `.env`
2. Ensure the `X-API-Key` header is included in requests
3. Verify the API key matches exactly (no extra spaces)

### Issue: Rate Limit Exceeded

**Solution:**
1. Wait for the rate limit window to reset (1 minute)
2. Increase `RATE_LIMIT_PER_MINUTE` in `.env`
3. Use different IP addresses for higher throughput

### Issue: Tavily API Not Working

**Solution**: The agent has built-in fallback mechanisms. If Tavily isn't available:
- Trend analysis uses mock data
- Keyword research provides basic suggestions
- Competitor analysis uses alternative methods

To enable Tavily:
1. Get API key from [tavily.com](https://tavily.com)
2. Add to `.env`: `TAVILY_API_KEY=your_key`

### Issue: Empty Results

**Possible causes:**
- Missing OpenAI API key
- Invalid query format
- Network issues

**Solution:**
- Check `.env` file has valid `OPENAI_API_KEY`
- Review logs in `output/content_research_strategy_log_*.txt`
- Ensure internet connectivity

### Issue: Tool Not Called

**Possible causes:**
- Query too vague
- Mode detection error

**Solution:**
- Make query more specific
- Explicitly mention what you need (e.g., "research keywords for...")
- Use comprehensive mode

## 📝 Example Response

```json
{
  "status": "completed",
  "query": "Generate blog post ideas about AI automation for small businesses",
  "mode": "idea_generation",
  "ideation_result": "### Executive Summary\n\nThe growing trend of AI automation...",
  "data": {
    "trends": {...},
    "keywords": {...},
    "content_ideas": {...},
    "competitors": {...},
    "seo": {...}
  },
  "timestamp": "2025-12-06T10:00:00"
}
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Using Docker

See [FASTAPI_SETUP.md](FASTAPI_SETUP.md) for Docker deployment instructions.

## 📁 Project Structure

```
content_research_strategy_agent/
├── main.py                      # FastAPI application
├── content_ideation_agent.py    # LangGraph agent implementation
├── tools/                       # Content research and strategy tools
│   ├── trend_analyzer.py
│   ├── keyword_research.py
│   ├── content_generator.py
│   ├── competitor_analysis.py
│   └── seo_optimizer.py
├── output/                      # Generated results and logs
├── requirements.txt             # Python dependencies
├── start_api.sh                 # Startup script
├── API_USAGE.md                 # Detailed API documentation
├── FASTAPI_SETUP.md             # Setup and deployment guide
└── README.md                    # This file
```

## 🤝 Contributing

Contributions are welcome! To add new features:

1. Create new tools in `tools/` directory
2. Update state definition if needed
3. Add to README documentation
4. Test thoroughly with the API endpoints

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com) and [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [OpenAI](https://openai.com)
- API framework: [FastAPI](https://fastapi.tiangolo.com)
- Trend data from [Tavily](https://tavily.com)

## 📞 Support

For issues or questions:
- Check the logs in `output/` directory
- Review [API_USAGE.md](API_USAGE.md) for API documentation
- Review [FASTAPI_SETUP.md](FASTAPI_SETUP.md) for setup details
- Ensure API keys are valid
- Try comprehensive mode for best results

---

**Built with ❤️ using LangGraph and FastAPI**

Start generating amazing content ideas today! 🚀
# content-research-and-strategy-ai-agent
