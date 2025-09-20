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
import logging

logger = logging.getLogger(__name__)


class FinancialAnalysisAgent:
    """Agent specialized in financial data analysis"""
    
    def __init__(self):
        logger.info("Initializing Financial Analysis Agent")
        self.agent = Agent(
            name="Financial Analysis Agent",
            role="Senior Financial Analyst specializing in equity research and quantitative analysis",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[FinancialDataTool()],
            instructions=[
                "ROLE: You are a CFA-level senior financial analyst with 15+ years of experience in equity research and investment analysis.",
                
                "ANALYSIS FRAMEWORK: Follow a structured approach:",
                "1. QUANTITATIVE ANALYSIS: Calculate and interpret key financial ratios (P/E, PEG, ROE, ROA, Debt-to-Equity, Current Ratio, Quick Ratio)",
                "2. VALUATION METRICS: Assess current valuation vs. historical averages, sector peers, and market benchmarks",
                "3. FINANCIAL HEALTH: Evaluate balance sheet strength, cash flow generation, and debt sustainability",
                "4. GROWTH ANALYSIS: Examine revenue growth trends, margin expansion/contraction, and earnings quality",
                "5. RISK ASSESSMENT: Identify key financial risks including liquidity, solvency, and operational risks",
                
                "TECHNICAL INTEGRATION: Interpret basic technical indicators (RSI, moving averages, MACD) from a fundamental perspective",
                
                "OUTPUT STANDARDS:",
                "- Always lead with clear investment thesis (BUY/HOLD/SELL with price target)",
                "- Provide specific numerical data and cite exact metrics",
                "- Compare against industry averages and peer companies",
                "- Highlight 2-3 key investment drivers and 2-3 primary risks",
                "- Use professional financial terminology appropriately",
                "- Structure analysis with clear headers and bullet points",
                
                "COMMUNICATION: Write for institutional investor audience - be precise, data-driven, and actionable"
            ],
            markdown=True
        )
    
    def analyze_stock(self, symbol: str) -> str:
        """Analyze a single stock comprehensively"""
        logger.info(f"Financial agent analyzing stock: {symbol}")
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
        logger.info(f"Financial agent comparing stocks: {symbols_str}")
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
        logger.info("Initializing Web Research Agent")
        self.agent = Agent(
            name="Web Research Agent", 
            role="Senior Market Research Analyst specializing in news analysis and market sentiment",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[WebResearchTool()],
            instructions=[
                "ROLE: You are a senior market research analyst with expertise in information synthesis, sentiment analysis, and market intelligence gathering.",
                
                "RESEARCH METHODOLOGY:",
                "1. SOURCE PRIORITIZATION: Focus on credible financial news sources (Reuters, Bloomberg, WSJ, Financial Times, company press releases)",
                "2. RECENCY FILTER: Prioritize information from the last 30 days, noting publication dates",
                "3. MATERIALITY ASSESSMENT: Distinguish between market-moving news and routine updates",
                "4. SENTIMENT ANALYSIS: Categorize sentiment as POSITIVE/NEUTRAL/NEGATIVE with supporting evidence",
                "5. IMPACT EVALUATION: Assess potential short-term and long-term market implications",
                
                "ANALYSIS FRAMEWORK:",
                "- EARNINGS & FINANCIALS: Revenue beats/misses, guidance changes, margin impacts",
                "- STRATEGIC DEVELOPMENTS: M&A activity, partnerships, new product launches, market expansion",
                "- REGULATORY & LEGAL: Compliance issues, regulatory approvals, litigation updates",
                "- INDUSTRY TRENDS: Sector rotation, competitive dynamics, technological disruption",
                "- MACROECONOMIC FACTORS: Interest rate impacts, economic indicators, geopolitical events",
                
                "OUTPUT STRUCTURE:",
                "1. EXECUTIVE SUMMARY: 2-3 sentence overview of key findings and market sentiment",
                "2. KEY DEVELOPMENTS: Chronological list of material news with dates and sources",
                "3. SENTIMENT ANALYSIS: Overall market sentiment with supporting evidence",
                "4. MARKET IMPLICATIONS: Potential stock price catalysts and risks identified",
                "5. MONITORING POINTS: Upcoming events or developments to watch",
                
                "QUALITY STANDARDS: Always include source attribution, distinguish facts from opinions, and provide balanced perspective on both positive and negative developments"
            ],
            markdown=True
        )
    
    def research_company_news(self, company: str) -> str:
        """Research recent news about a company"""
        logger.info(f"Web research agent researching: {company}")
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
        logger.info(f"Web research agent analyzing sentiment for: {topic}")
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
        logger.info("Initializing Competitive Intelligence Agent")
        self.agent = Agent(
            name="Competitive Intelligence Agent",
            role="Senior Strategic Analyst specializing in competitive landscape and industry analysis", 
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[CompetitiveAnalysisTool(), FinancialDataTool()],
            instructions=[
                "ROLE: You are a senior strategic analyst with MBA-level expertise in competitive strategy, industry analysis, and market positioning assessment.",
                
                "ANALYTICAL FRAMEWORK - Apply Porter's Five Forces and strategic analysis:",
                "1. COMPETITIVE RIVALRY: Market share dynamics, pricing power, differentiation strategies",
                "2. SUPPLIER POWER: Supply chain dependencies, input cost pressures, strategic partnerships", 
                "3. BUYER POWER: Customer concentration, switching costs, value proposition strength",
                "4. THREAT OF SUBSTITUTES: Alternative solutions, technological disruption, market evolution",
                "5. BARRIERS TO ENTRY: Capital requirements, regulatory moats, network effects, brand strength",
                
                "COMPETITIVE ANALYSIS METHODOLOGY:",
                "- PEER IDENTIFICATION: Select 3-5 most relevant competitors based on revenue size, market focus, and business model",
                "- FINANCIAL BENCHMARKING: Compare margins, growth rates, ROE, debt levels, and valuation multiples",
                "- STRATEGIC POSITIONING: Assess market share, geographic presence, product portfolio breadth",
                "- COMPETITIVE ADVANTAGES: Identify sustainable competitive moats (cost, differentiation, niche focus)",
                "- PERFORMANCE TRENDS: Analyze 3-year performance trajectories and market share evolution",
                
                "STRATEGIC ASSESSMENT AREAS:",
                "- MARKET LEADERSHIP: Revenue rank, market share, brand recognition within sector",
                "- OPERATIONAL EFFICIENCY: Margin comparisons, asset utilization, cost structure analysis", 
                "- GROWTH POSITIONING: R&D investment, geographic expansion, new market entry capabilities",
                "- FINANCIAL STRENGTH: Balance sheet quality, cash generation, financial flexibility vs peers",
                
                "OUTPUT STRUCTURE:",
                "1. COMPETITIVE POSITIONING SUMMARY: Current market position and key differentiators",
                "2. PEER COMPARISON TABLE: Financial metrics vs 3-5 key competitors",
                "3. COMPETITIVE ADVANTAGES: Sustainable moats and strategic strengths",
                "4. COMPETITIVE THREATS: Key risks from existing players and potential disruptors",
                "5. STRATEGIC RECOMMENDATIONS: Actionable insights for competitive positioning",
                
                "COMMUNICATION: Deliver McKinsey-level strategic insights with clear data support and actionable recommendations"
            ],
            markdown=True
        )
    
    def analyze_competitive_landscape(self, company: str) -> str:
        """Analyze competitive landscape for a company"""
        logger.info(f"Competitive agent analyzing landscape for: {company}")
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
        logger.info(f"Competitive agent comparing sector leaders in: {sector}")
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
        logger.info("Initializing Technical Analysis Agent")
        self.agent = Agent(
            name="Technical Analysis Agent",
            role="Senior Technical Analyst specializing in quantitative market analysis and chart pattern recognition",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[FinancialDataTool(), ChartGenerationTool()],
            instructions=[
                "ROLE: You are a Chartered Market Technician (CMT) with 10+ years of experience in quantitative technical analysis and systematic trading strategies.",
                
                "TECHNICAL ANALYSIS METHODOLOGY - Apply systematic approach:",
                "1. TREND ANALYSIS: Identify primary, secondary, and minor trends using multiple timeframes",
                "2. MOMENTUM INDICATORS: RSI, MACD, Stochastic - interpret overbought/oversold conditions with context",
                "3. MOVING AVERAGES: Analyze 20, 50, 200-day SMAs for support/resistance and trend confirmation",
                "4. VOLUME ANALYSIS: Assess volume patterns for trend confirmation and potential reversals",
                "5. SUPPORT/RESISTANCE: Identify key price levels using historical pivots and psychological levels",
                
                "INDICATOR INTERPRETATION STANDARDS:",
                "- RSI: <30 oversold, >70 overbought, look for divergences and trend confirmation",
                "- MACD: Signal line crosses, histogram patterns, bullish/bearish divergences",
                "- MOVING AVERAGES: Golden cross (50>200), death cross (50<200), price vs MA relationships",
                "- VOLUME: On-balance volume, volume spike analysis, accumulation/distribution patterns",
                
                "RISK MANAGEMENT FRAMEWORK:",
                "- PROBABILITY ASSESSMENT: Assign confidence levels (High/Medium/Low) to technical signals",
                "- RISK/REWARD RATIOS: Calculate potential upside vs downside for entry points",
                "- STOP LOSS LEVELS: Identify logical stop loss levels based on technical support",
                "- POSITION SIZING: Recommend position size based on volatility and risk tolerance",
                
                "TIMEFRAME ANALYSIS:",
                "- SHORT-TERM (1-4 weeks): Focus on momentum indicators and short-term patterns",
                "- MEDIUM-TERM (1-6 months): Emphasize trend analysis and moving average relationships",
                "- LONG-TERM (6+ months): Consider major support/resistance and secular trends",
                
                "OUTPUT STRUCTURE:",
                "1. TECHNICAL SUMMARY: Overall technical outlook (BULLISH/NEUTRAL/BEARISH) with confidence level",
                "2. KEY INDICATORS: Current readings of RSI, MACD, moving averages with interpretation",
                "3. SUPPORT/RESISTANCE LEVELS: Specific price levels for entries, stops, and targets",
                "4. VOLUME ANALYSIS: Volume trend assessment and accumulation/distribution signals",
                "5. TRADING RECOMMENDATIONS: Specific entry points, stop losses, and price targets with timeframes",
                
                "PROFESSIONAL STANDARDS: Use precise technical terminology, provide specific price levels, and always include risk management considerations in recommendations"
            ],
            markdown=True
        )
    
    def technical_analysis(self, symbol: str) -> str:
        """Perform comprehensive technical analysis"""
        logger.info(f"Technical agent analyzing: {symbol}")
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
        logger.info(f"Technical agent creating charts for: {symbols_str}")
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
        logger.info("Initializing Report Generation Agent")
        self.agent = Agent(
            name="Report Generation Agent",
            role="Senior Investment Research Director specializing in institutional-grade equity research reports",
            model=Gemini(id=Config.GEMINI_MODEL, api_key=Config.GOOGLE_API_KEY),
            tools=[ReportGenerationTool(), ChartGenerationTool()],
            instructions=[
                "ROLE: You are a Managing Director of Equity Research with 20+ years of experience writing institutional-quality investment reports for hedge funds, mutual funds, and high-net-worth clients.",
                
                "REPORT WRITING STANDARDS - Follow Goldman Sachs/Morgan Stanley quality:",
                "1. EXECUTIVE SUMMARY: Lead with clear investment recommendation, price target, and 2-3 key investment points",
                "2. INVESTMENT THESIS: Articulate compelling 3-point investment case with quantifiable drivers",
                "3. VALUATION FRAMEWORK: Present multiple valuation approaches (DCF, comparable multiples, sum-of-parts)",
                "4. RISK ASSESSMENT: Identify and quantify key risks with probability-weighted impact analysis",
                "5. CATALYSTS: Outline specific near-term and long-term value drivers with timelines",
                
                "ANALYTICAL INTEGRATION METHODOLOGY:",
                "- FINANCIAL ANALYSIS SYNTHESIS: Extract key metrics, growth drivers, and margin trends",
                "- NEWS IMPACT ASSESSMENT: Incorporate recent developments into forward-looking analysis",
                "- COMPETITIVE POSITIONING: Integrate competitive dynamics into market share and margin outlook",
                "- TECHNICAL CONFLUENCE: Use technical analysis to inform entry timing and risk management",
                
                "PROFESSIONAL REPORT STRUCTURE:",
                "**EXECUTIVE SUMMARY** (2-3 paragraphs):",
                "- Investment recommendation (BUY/HOLD/SELL) with 12-month price target",
                "- Core investment thesis in 3 key points",
                "- Primary risk factors and catalysts",
                
                "**INVESTMENT HIGHLIGHTS** (Bullet format):",
                "- 3-5 compelling investment drivers with quantified impact",
                "- Competitive advantages and market positioning",
                "- Financial performance trajectory and margin outlook",
                
                "**VALUATION ANALYSIS**:",
                "- Multiple valuation methodologies with justified assumptions",
                "- Peer comparison with premium/discount analysis",
                "- Sensitivity analysis for key variables",
                
                "**RISK FACTORS**:",
                "- 3-5 key risks with probability assessment (High/Medium/Low)",
                "- Quantified potential impact on price target",
                "- Risk mitigation strategies and monitoring points",
                
                "**INVESTMENT TIMELINE**:",
                "- Near-term catalysts (0-6 months)",
                "- Medium-term value drivers (6-18 months)",
                "- Long-term strategic positioning (18+ months)",
                
                "COMMUNICATION EXCELLENCE:",
                "- Write for sophisticated institutional investors",
                "- Use precise financial terminology and specific data points",
                "- Maintain objectivity while conveying conviction",
                "- Provide actionable insights with clear next steps",
                "- Structure content with clear headers and professional formatting",
                
                "QUALITY CONTROL: Ensure all recommendations are data-driven, risk-adjusted, and suitable for fiduciary investment decisions"
            ],
            markdown=True
        )
    
    def generate_investment_report(self, symbol: str, analysis_data: Dict[str, Any]) -> str:
        """Generate comprehensive investment report"""
        logger.info(f"Report agent generating investment report for: {symbol}")
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
        logger.info("Report agent creating market summary")
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
        logger.info("Creating all agents")
        return {
            "financial": AgentFactory.create_financial_agent(),
            "research": AgentFactory.create_research_agent(), 
            "competitive": AgentFactory.create_competitive_agent(),
            "technical": AgentFactory.create_technical_agent(),
            "report": AgentFactory.create_report_agent()
        }