from agno.agent import Agent
from agno.models.google import Gemini
from tools import (
    FinancialDataTool, 
    WebResearchTool, 
    CompetitiveAnalysisTool, 
    ChartGenerationTool, 
    ReportGenerationTool
)
from config import Config
from typing import Dict, Any


class FinancialAnalysisAgent:
    """Agent specialized in financial data analysis"""
    
    def __init__(self):
        self.agent = Agent(
            name="Financial Analysis Agent",
            role="Analyze financial data, calculate metrics, and provide investment insights",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[FinancialDataTool()],
            instructions=[
                "You are a financial analyst expert",
                "Provide detailed financial analysis with specific metrics",
                "Calculate and interpret financial ratios",
                "Focus on quantitative analysis",
                "Always include current market data",
                "Explain technical indicators in simple terms"
            ],
            markdown=True
        )
    
    def analyze_stock(self, symbol: str) -> str:
        """Analyze a single stock comprehensively"""
        prompt = f"""
        Perform a comprehensive financial analysis of {symbol}. Include:
        
        1. Current stock data and recent performance
        2. Key financial metrics (P/E, EPS, Market Cap, etc.)
        3. Technical indicators analysis
        4. Financial health assessment
        5. Investment recommendation based on data
        
        Use the available tools to gather real-time data.
        """
        return self.agent.run(prompt).content
    
    def compare_stocks(self, symbols: list) -> str:
        """Compare multiple stocks"""
        symbols_str = ", ".join(symbols)
        prompt = f"""
        Compare the following stocks: {symbols_str}
        
        Analyze:
        1. Current valuations and metrics
        2. Financial performance comparison
        3. Technical analysis for each
        4. Relative strengths and weaknesses
        5. Investment ranking and recommendations
        
        Use financial tools to get real data for comparison.
        """
        return self.agent.run(prompt).content


class WebResearchAgent:
    """Agent specialized in web research and news analysis"""
    
    def __init__(self):
        self.agent = Agent(
            name="Web Research Agent", 
            role="Research market news, trends, and sentiment analysis",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[WebResearchTool()],
            instructions=[
                "You are a market research analyst",
                "Search for current market news and trends",
                "Analyze sentiment from news sources",
                "Identify market-moving events",
                "Summarize key findings clearly",
                "Focus on recent and relevant information"
            ],
            markdown=True
        )
    
    def research_company_news(self, company: str) -> str:
        """Research recent news about a company"""
        prompt = f"""
        Research recent news and developments about {company}. 
        
        Find and analyze:
        1. Recent news articles (last 30 days)
        2. Major announcements or events
        3. Market sentiment analysis
        4. Industry trends affecting the company
        5. Overall news impact on stock performance
        
        Use web search tools to gather current information.
        """
        return self.agent.run(prompt).content
    
    def analyze_market_sentiment(self, topic: str) -> str:
        """Analyze market sentiment on a specific topic"""
        prompt = f"""
        Analyze current market sentiment regarding {topic}.
        
        Research:
        1. Recent market discussions and news
        2. Analyst opinions and reports
        3. Social media and forum sentiment
        4. Overall market mood and trends
        5. Potential impact on related stocks
        
        Use search tools to gather diverse perspectives.
        """
        return self.agent.run(prompt).content


class CompetitiveIntelligenceAgent:
    """Agent specialized in competitive analysis"""
    
    def __init__(self):
        self.agent = Agent(
            name="Competitive Intelligence Agent",
            role="Analyze competitive landscape and market positioning", 
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[CompetitiveAnalysisTool(), FinancialDataTool()],
            instructions=[
                "You are a competitive analysis expert",
                "Compare companies within industries",
                "Identify competitive advantages and threats",
                "Analyze market share and positioning",
                "Provide strategic insights",
                "Focus on relative performance metrics"
            ],
            markdown=True
        )
    
    def analyze_competitive_landscape(self, company: str) -> str:
        """Analyze competitive landscape for a company"""
        prompt = f"""
        Analyze the competitive landscape for {company}.
        
        Perform:
        1. Identify main competitors in the same sector
        2. Compare financial performance vs competitors
        3. Analyze competitive advantages and weaknesses
        4. Market share and positioning analysis
        5. Competitive threats and opportunities
        
        Use competitive analysis tools to gather comparison data.
        """
        return self.agent.run(prompt).content
    
    def compare_sector_leaders(self, sector: str) -> str:
        """Compare leading companies in a sector"""
        prompt = f"""
        Compare the leading companies in the {sector} sector.
        
        Analyze:
        1. Top companies by market cap and performance
        2. Financial metrics comparison
        3. Competitive positioning
        4. Growth prospects and strategies
        5. Investment attractiveness ranking
        
        Use tools to get real financial data for comparison.
        """
        return self.agent.run(prompt).content


class TechnicalAnalysisAgent:
    """Agent specialized in technical analysis"""
    
    def __init__(self):
        self.agent = Agent(
            name="Technical Analysis Agent",
            role="Perform technical analysis and chart pattern recognition",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[FinancialDataTool(), ChartGenerationTool()],
            instructions=[
                "You are a technical analysis expert",
                "Analyze price patterns and technical indicators",
                "Identify support and resistance levels",
                "Interpret trading signals",
                "Provide short-term trading insights",
                "Explain technical concepts clearly"
            ],
            markdown=True
        )
    
    def technical_analysis(self, symbol: str) -> str:
        """Perform comprehensive technical analysis"""
        prompt = f"""
        Perform detailed technical analysis for {symbol}.
        
        Analyze:
        1. Current technical indicators (RSI, MACD, Moving Averages)
        2. Price trends and momentum
        3. Support and resistance levels
        4. Trading volume analysis
        5. Short-term and medium-term outlook
        6. Entry/exit points for traders
        
        Use technical analysis tools and generate relevant charts.
        """
        return self.agent.run(prompt).content
    
    def chart_analysis(self, symbols: list) -> str:
        """Generate and analyze charts for multiple symbols"""
        symbols_str = ", ".join(symbols)
        prompt = f"""
        Generate and analyze charts for: {symbols_str}
        
        Create:
        1. Individual price charts with technical indicators
        2. Comparative performance chart
        3. Technical pattern identification
        4. Trend analysis and projections
        5. Trading recommendations based on charts
        
        Use chart generation tools to create visualizations.
        """
        return self.agent.run(prompt).content


class ReportGenerationAgent:
    """Agent specialized in synthesizing analysis into comprehensive reports"""
    
    def __init__(self):
        self.agent = Agent(
            name="Report Generation Agent",
            role="Synthesize analysis from multiple sources into comprehensive reports",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[ReportGenerationTool(), ChartGenerationTool()],
            instructions=[
                "You are a senior investment analyst and report writer",
                "Synthesize information from multiple sources",
                "Create clear, actionable investment reports",
                "Structure information logically",
                "Provide specific recommendations with rationale",
                "Use professional investment analysis language"
            ],
            markdown=True
        )
    
    def generate_investment_report(self, symbol: str, analysis_data: Dict[str, Any]) -> str:
        """Generate comprehensive investment report"""
        prompt = f"""
        Generate a comprehensive investment analysis report for {symbol} using the provided analysis data.
        
        Structure the report with:
        1. Executive Summary with clear recommendation
        2. Financial Analysis highlights
        3. Technical Analysis summary
        4. Competitive Position assessment
        5. Market News and Sentiment impact
        6. Risk Assessment
        7. Price Target and Investment Thesis
        
        Analysis Data:
        {analysis_data}
        
        Create a professional report suitable for investment decision-making.
        """
        return self.agent.run(prompt).content
    
    def create_market_summary(self, market_data: Dict[str, Any]) -> str:
        """Create market summary report"""
        prompt = f"""
        Create a comprehensive market summary report using the provided data.
        
        Include:
        1. Market Overview and key themes
        2. Sector Performance Analysis
        3. Notable Company Highlights
        4. Technical Market Conditions
        5. News and Sentiment Summary
        6. Investment Opportunities and Risks
        
        Market Data:
        {market_data}
        
        Present as a professional market briefing.
        """
        return self.agent.run(prompt).content


# Agent Factory
class AgentFactory:
    """Factory class to create and manage agents"""
    
    @staticmethod
    def create_financial_agent():
        return FinancialAnalysisAgent()
    
    @staticmethod
    def create_research_agent():
        return WebResearchAgent()
    
    @staticmethod
    def create_competitive_agent():
        return CompetitiveIntelligenceAgent()
    
    @staticmethod
    def create_technical_agent():
        return TechnicalAnalysisAgent()
    
    @staticmethod
    def create_report_agent():
        return ReportGenerationAgent()
    
    @staticmethod
    def create_all_agents():
        """Create all agents for use in workflows"""
        return {
            "financial": AgentFactory.create_financial_agent(),
            "research": AgentFactory.create_research_agent(), 
            "competitive": AgentFactory.create_competitive_agent(),
            "technical": AgentFactory.create_technical_agent(),
            "report": AgentFactory.create_report_agent()
        }