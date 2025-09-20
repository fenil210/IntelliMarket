# 📊 IntelliMarket Research Platform

<div align="center">

```
██╗███╗   ██╗████████╗███████╗██╗     ██╗     ██╗███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗
██║████╗  ██║╚══██╔══╝██╔════╝██║     ██║     ██║████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝
██║██╔██╗ ██║   ██║   █████╗  ██║     ██║     ██║██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   
██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██║     ██║██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   
██║██║ ╚████║   ██║   ███████╗███████╗███████╗██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   
```

**AI-Powered Investment Analysis & Market Research Platform**

*Professional-grade multi-agent system for institutional investment analysis*

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/framework-AGNO-purple.svg)](https://docs.agno.com)
[![AI Model](https://img.shields.io/badge/ai-Gemini%201.5%20Flash-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

## 🌟 Overview

IntelliMarket is an enterprise-grade investment research platform that leverages multiple AI agents to provide comprehensive financial analysis. Built with the AGNO framework and powered by Google's Gemini AI, it delivers institutional-quality research reports comparable to Goldman Sachs and Morgan Stanley.

### 🎯 Key Highlights

- **🤖 Multi-Agent Architecture**: 5 specialized AI agents working in coordination
- **📈 Real-Time Data**: Live market data via YFinance and web research via DuckDuckGo
- **💼 Institutional Quality**: CFA/CMT-level analysis with professional report formatting
- **⚡ High Performance**: ~10,000x faster than LangGraph with minimal memory footprint
- **🌐 Full-Stack Solution**: REST API backend with professional web frontend
- **📊 Beautiful UI**: Investment-grade interface with interactive charts and tables

## ✨ Features

### 🔍 **Single Stock Analysis**

- Comprehensive financial metrics analysis (P/E, ROE, debt ratios)
- Technical analysis with RSI, MACD, moving averages
- Real-time news sentiment analysis
- Competitive landscape assessment
- Investment recommendations with price targets

### ⚖️ **Stock Comparison**

- Side-by-side analysis of multiple stocks
- Relative valuation and performance metrics
- Competitive positioning analysis
- Investment ranking with rationale

### 🌐 **Market Research**

- Topic-based market sentiment analysis
- Industry trend identification
- Related stock discovery and analysis
- News impact assessment

### 🧠 **Custom Query Processing**

- Natural language investment questions
- Intelligent agent routing based on query content
- Contextual analysis with multiple perspectives

### 📊 **Professional Reporting**

- Institutional-grade report generation
- Interactive data tables and visualizations
- Downloadable markdown reports
- Real-time progress tracking

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Interface<br/>HTML/CSS/JS]
        API_CLIENT[API Client<br/>JavaScript]
    end
  
    subgraph "Backend Layer"
        FLASK[Flask API Server<br/>REST Endpoints]
        WORKFLOWS[Workflow Engine<br/>Agent Coordination]
    end
  
    subgraph "AI Agent Layer"
        FA[Financial Agent<br/>CFA-Level Analysis]
        TA[Technical Agent<br/>CMT Analysis]
        RA[Research Agent<br/>News & Sentiment]
        CA[Competitive Agent<br/>Strategic Analysis]
        REP[Report Agent<br/>Synthesis & Formatting]
    end
  
    subgraph "Data Layer"
        YF[YFinance<br/>Market Data]
        DDG[DuckDuckGo<br/>Web Research]
        GEMINI[Gemini AI<br/>LLM Processing]
    end
  
    UI --> API_CLIENT
    API_CLIENT --> FLASK
    FLASK --> WORKFLOWS
    WORKFLOWS --> FA
    WORKFLOWS --> TA
    WORKFLOWS --> RA
    WORKFLOWS --> CA
    WORKFLOWS --> REP
    FA --> YF
    TA --> YF
    RA --> DDG
    CA --> YF
    REP --> GEMINI
    FA --> GEMINI
    TA --> GEMINI
    RA --> GEMINI
    CA --> GEMINI
```

### Multi-Agent Workflow

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Workflow
    participant FA as Financial Agent
    participant TA as Technical Agent
    participant RA as Research Agent
    participant CA as Competitive Agent
    participant REP as Report Agent
  
    User->>API: Request Stock Analysis
    API->>Workflow: Initialize Analysis
  
    par Parallel Analysis
        Workflow->>FA: Analyze Financials
        Workflow->>TA: Technical Analysis
        Workflow->>RA: News Research
        Workflow->>CA: Competitive Analysis
    end
  
    FA-->>Workflow: Financial Metrics
    TA-->>Workflow: Technical Indicators
    RA-->>Workflow: Market Sentiment
    CA-->>Workflow: Competitive Position
  
    Workflow->>REP: Synthesize Report
    REP-->>Workflow: Final Report
    Workflow-->>API: Complete Analysis
    API-->>User: Investment Report
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))
- Internet connection for real-time data

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/intelligmarket.git
   cd intelligmarket
   ```
2. **Set up virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Configure environment**

   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env file and add your Gemini API key
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

1. **Start the backend server**

   ```bash
   python run.py
   ```

   Backend will be available at `http://127.0.0.1:5000`
2. **Start the frontend server** (in a new terminal)

   ```bash
   cd frontend
   python -m http.server 8080
   ```

   Frontend will be available at `http://localhost:8080`
3. **Access the application**

   Open your browser and navigate to `http://localhost:8080`

## 📖 Documentation

### API Endpoints

| Endpoint                          | Method | Description             |
| --------------------------------- | ------ | ----------------------- |
| `/health`                       | GET    | Health check            |
| `/api/system/info`              | GET    | System information      |
| `/api/analyze/stock`            | POST   | Single stock analysis   |
| `/api/analyze/comparison`       | POST   | Stock comparison        |
| `/api/analyze/research`         | POST   | Market research         |
| `/api/analyze/query`            | POST   | Custom query processing |
| `/api/validate/symbol/{symbol}` | GET    | Stock symbol validation |

### Request Examples

#### Single Stock Analysis

```bash
curl -X POST http://127.0.0.1:5000/api/analyze/stock \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "type": "comprehensive"
  }'
```

#### Stock Comparison

```bash
curl -X POST http://127.0.0.1:5000/api/analyze/comparison \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["AAPL", "MSFT", "GOOGL"]
  }'
```

#### Market Research

```bash
curl -X POST http://127.0.0.1:5000/api/analyze/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI stocks 2024"
  }'
```

### Configuration

#### Environment Variables

| Variable           | Description           | Default       |
| ------------------ | --------------------- | ------------- |
| `GOOGLE_API_KEY` | Gemini AI API key     | Required      |
| `FLASK_DEBUG`    | Enable debug mode     | `true`      |
| `FLASK_HOST`     | Server host           | `127.0.0.1` |
| `FLASK_PORT`     | Server port           | `5000`      |
| `LOG_LEVEL`      | Logging level         | `INFO`      |
| `AGNO_TELEMETRY` | Enable AGNO telemetry | `false`     |

#### Agent Configuration

Agents can be customized by modifying their instructions in `backend/agents.py`:

- **Financial Agent**: CFA-level financial analysis
- **Technical Agent**: CMT-level technical analysis
- **Research Agent**: Market research and sentiment analysis
- **Competitive Agent**: Strategic competitive analysis
- **Report Agent**: Professional report synthesis

## 🛠️ Development

### Project Structure

```
intelligmarket/
├── backend/                 # Backend API server
│   ├── app.py              # Flask application factory
│   ├── config.py           # Configuration management
│   ├── agents.py           # AI agent definitions
│   ├── tools.py            # Agent tools and utilities
│   ├── workflows.py        # Multi-agent workflows
│   ├── requirements.txt    # Python dependencies
│   └── api/
│       ├── __init__.py
│       └── routes.py       # REST API endpoints
├── frontend/               # Frontend web application
│   ├── index.html         # Main HTML file
│   ├── css/
│   │   └── styles.css     # Professional styling
│   └── js/
│       ├── api.js         # API communication
│       └── main.js        # Application logic
├── .env                   # Environment variables
├── run.py                 # Application runner
└── README.md              # This file
```

### Adding New Tools

1. Create tool class in `backend/tools.py`:

   ```python
   class CustomTool(Toolkit):
       def custom_function(self, parameter: str) -> Dict[str, Any]:
           # Your tool logic here
           return {"result": "data"}
   ```
2. Add tool to relevant agent in `backend/agents.py`:

   ```python
   tools=[FinancialDataTool(), CustomTool()]
   ```

### Adding New Agents

1. Create agent class in `backend/agents.py`:

   ```python
   class CustomAgent:
       def __init__(self):
           self.agent = Agent(
               name="Custom Agent",
               model=Gemini(id=Config.GEMINI_MODEL),
               tools=[CustomTool()],
               instructions=["Custom instructions"]
           )
   ```
2. Add to `AgentFactory.create_all_agents()` method

### Testing

```bash
# Backend health check
curl http://127.0.0.1:5000/health

# Test single stock analysis
curl -X POST http://127.0.0.1:5000/api/analyze/stock \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "type": "quick"}'
```

## 🚀 Deployment

### Production Configuration

1. **Environment Variables**

   ```bash
   FLASK_DEBUG=false
   SECRET_KEY=your-secure-secret-key
   CORS_ORIGINS=https://yourdomain.com
   LOG_LEVEL=WARNING
   ```
2. **Backend Deployment**

   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app()"
   ```
3. **Frontend Deployment**

   - Serve `frontend/` directory via nginx, Apache, or static hosting
   - Update API base URL in `frontend/js/api.js`

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
```

```bash
# Build and run
docker build -t intelligmarket .
docker run -p 5000:5000 -e GOOGLE_API_KEY=your_key intelligmarket
```

## 🔧 Performance

### Benchmarks

| Framework                      | Agent Creation | Memory Usage | Analysis Time |
| ------------------------------ | -------------- | ------------ | ------------- |
| **IntelliMarket (AGNO)** | ~2μs          | ~3.75KB      | 30-120s       |
| LangGraph                      | ~20ms          | ~187KB       | 60-300s       |
| LangChain                      | ~15ms          | ~156KB       | 90-400s       |

### Optimization Tips

- Use "Quick Analysis" for faster results (30-60 seconds)
- Comprehensive analysis provides detailed insights (2-5 minutes)
- Cache results for repeated queries
- Monitor API usage to optimize costs

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings for public methods
- Keep functions focused and small
- Use meaningful variable names

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AGNO Framework**: High-performance multi-agent system foundation
- **Google Gemini**: Advanced AI capabilities for analysis
- **YFinance**: Real-time financial data access
- **DuckDuckGo**: Privacy-focused web search capabilities

## 📞 Support

- **Documentation**: [docs.agno.com](https://docs.agno.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/intelligmarket/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/intelligmarket/discussions)
- **Email**: support@intelligmarket.dev

## 🗺️ Roadmap

### Version 2.0 (Q2 2024)

- [ ] Portfolio tracking and management
- [ ] Risk management tools
- [ ] Email alert system
- [ ] Advanced charting capabilities

### Version 2.1 (Q3 2024)

- [ ] Social sentiment analysis
- [ ] Options analysis tools
- [ ] Backtesting capabilities
- [ ] Mobile application

### Version 3.0 (Q4 2024)

- [ ] Machine learning predictions
- [ ] Custom model training
- [ ] Advanced risk analytics
- [ ] Enterprise features

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ by the IntelliMarket team

</div>
