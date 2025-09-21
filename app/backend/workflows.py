from typing import Dict, List, Any
from agents import AgentFactory
from datetime import datetime
import json
import logging
import re

logger = logging.getLogger(__name__)


class InvestmentAnalysisWorkflow:
    """Workflow for comprehensive investment analysis"""
    
    def __init__(self):
        logger.info("Initializing Investment Analysis Workflow")
        self.agents = AgentFactory.create_all_agents()
        self.results = {}
    
    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Complete stock analysis workflow"""
        
        logger.info(f"Starting comprehensive analysis for {symbol}")
        
        # Step 1: Financial Analysis
        logger.info("Performing financial analysis")
        financial_analysis = self.agents["financial"].analyze_stock(symbol)
        
        # Debug: Check for $1 in financial analysis
        if isinstance(financial_analysis, str) and "$1" in financial_analysis:
            logger.warning(f"WARNING: $1 detected in financial analysis for {symbol}")
            # Try to get debug data
            debug_data = self.agents["financial"].debug_tool_data(symbol)
            logger.warning(f"Debug tool data: {debug_data}")
        
        self.results["financial"] = financial_analysis
        
        # Step 2: Technical Analysis  
        logger.info("Performing technical analysis")
        technical_analysis = self.agents["technical"].technical_analysis(symbol)
        self.results["technical"] = technical_analysis
        
        # Step 3: News Research
        logger.info("Researching company news")
        news_analysis = self.agents["research"].research_company_news(symbol)
        self.results["news"] = news_analysis
        
        # Step 4: Competitive Analysis
        logger.info("Analyzing competitive landscape")
        competitive_analysis = self.agents["competitive"].analyze_competitive_landscape(symbol)
        self.results["competitive"] = competitive_analysis
        
        # Step 5: Generate Final Report
        logger.info("Generating comprehensive report")
        final_report = self.agents["report"].generate_investment_report(
            symbol, 
            {
                "financial_analysis": financial_analysis,
                "technical_analysis": technical_analysis,
                "news_analysis": news_analysis,
                "competitive_analysis": competitive_analysis,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Debug: Check for $1 in final report
        if isinstance(final_report, str) and "$1" in final_report:
            logger.warning(f"WARNING: $1 detected in final report for {symbol}")
        
        self.results["final_report"] = final_report
        
        logger.info("Analysis complete")
        
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "financial_analysis": financial_analysis,
            "technical_analysis": technical_analysis,
            "news_analysis": news_analysis,
            "competitive_analysis": competitive_analysis,
            "final_report": final_report
        }
    
    def quick_analysis(self, symbol: str) -> str:
        """Quick analysis for faster results"""
        logger.info(f"Quick analysis for {symbol}")
        
        # Debug: Test tool data before analysis
        debug_data = self.agents["financial"].debug_tool_data(symbol)
        current_price = debug_data.get('current_price')
        logger.info(f"DEBUG: Tool data before quick analysis: current_price = {current_price}")
        
        # Just financial and technical analysis
        financial = self.agents["financial"].analyze_stock(symbol)
        technical = self.agents["technical"].technical_analysis(symbol)
        
        # Debug: Check for $1 in analysis results
        if isinstance(financial, str) and "$1" in financial:
            logger.warning(f"WARNING: $1 detected in quick financial analysis for {symbol}")
            # Force replace with real price if available
            if current_price:
                logger.warning(f"Forcing replacement of $1 with ${current_price}")
                financial = financial.replace("$1", f"${current_price}")
        
        # Generate quick report
        report = self.agents["report"].generate_investment_report(
            symbol,
            {
                "financial_analysis": financial,
                "technical_analysis": technical,
                "analysis_type": "quick",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Final safety check: replace any remaining $1 with real price
        if isinstance(report, str) and "$1" in report and current_price:
            logger.warning(f"FINAL CLEANUP: Replacing remaining $1 with ${current_price} in report for {symbol}")
            report = report.replace("$1", f"${current_price}")
        
        # Debug: Check final report
        if isinstance(report, str) and "$1" in report:
            logger.error(f"CRITICAL: $1 still detected in final quick report for {symbol}")
        
        logger.info("Quick analysis complete")
        return report


class ComparisonWorkflow:
    """Workflow for comparing multiple stocks"""
    
    def __init__(self):
        logger.info("Initializing Comparison Workflow")
        self.agents = AgentFactory.create_all_agents()
    
    def compare_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple stocks across different dimensions"""
        
        logger.info(f"Comparing stocks: {', '.join(symbols)}")
        
        results = {}
        
        # Debug: Test tool data for all symbols first
        for symbol in symbols:
            debug_data = self.agents["financial"].debug_tool_data(symbol)
            logger.info(f"DEBUG: Tool data for {symbol} before comparison: current_price = {debug_data.get('current_price')}")
        
        # Financial Comparison
        logger.info("Financial comparison")
        financial_comparison = self.agents["financial"].compare_stocks(symbols)
        
        # Debug: Check for $1 in financial comparison
        if isinstance(financial_comparison, str) and "$1" in financial_comparison:
            logger.warning(f"WARNING: $1 detected in financial comparison for {symbols}")
        
        results["financial_comparison"] = financial_comparison
        
        # Technical Comparison
        logger.info("Technical comparison")
        technical_comparison = self.agents["technical"].chart_analysis(symbols)
        results["technical_comparison"] = technical_comparison
        
        # Competitive Analysis for each stock
        logger.info("Competitive analysis")
        competitive_analyses = {}
        for symbol in symbols:
            competitive_analyses[symbol] = self.agents["competitive"].analyze_competitive_landscape(symbol)
        results["competitive_analyses"] = competitive_analyses
        
        # Generate comparison report
        logger.info("Generating comparison report")
        comparison_report = self.agents["report"].create_market_summary({
            "symbols": symbols,
            "financial_comparison": financial_comparison,
            "technical_comparison": technical_comparison,
            "competitive_analyses": competitive_analyses,
            "analysis_type": "comparison",
            "timestamp": datetime.now().isoformat()
        })
        results["comparison_report"] = comparison_report
        
        logger.info("Comparison complete")
        
        return results


class MarketResearchWorkflow:
    """Workflow for market research and sentiment analysis"""
    
    def __init__(self):
        logger.info("Initializing Market Research Workflow")
        self.agents = AgentFactory.create_all_agents()
    
    def research_market_topic(self, topic: str) -> Dict[str, Any]:
        """Research a specific market topic or trend"""
        
        logger.info(f"Researching market topic: {topic}")
        
        results = {}
        
        # Web research for the topic
        logger.info("Web research")
        web_research = self.agents["research"].analyze_market_sentiment(topic)
        
        # Debug: Check the type and content of web research
        logger.info(f"DEBUG: Web research result type: {type(web_research)}")
        logger.info(f"DEBUG: Web research preview: {str(web_research)[:200]}...")
        
        results["web_research"] = web_research
        
        # If topic contains stock symbols, analyze them
        potential_symbols = self._extract_symbols(topic)
        if potential_symbols:
            logger.info(f"Found potential stocks: {potential_symbols}")
            financial_context = {}
            for symbol in potential_symbols[:3]:
                financial_context[symbol] = self.agents["financial"].analyze_stock(symbol)
            results["financial_context"] = financial_context
        
        # Generate research report
        logger.info("Generating research report")
        research_report = self.agents["report"].create_market_summary({
            "topic": topic,
            "web_research": web_research,
            "financial_context": results.get("financial_context", {}),
            "analysis_type": "market_research",
            "timestamp": datetime.now().isoformat()
        })
        
        # Debug: Check the research report
        logger.info(f"DEBUG: Research report type: {type(research_report)}")
        logger.info(f"DEBUG: Research report preview: {str(research_report)[:200]}...")
        
        results["research_report"] = research_report
        
        logger.info("Market research complete")
        
        # Return the research report directly as a string for frontend compatibility
        return {
            "web_research": web_research,
            "research_report": research_report,
            "financial_context": results.get("financial_context", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_symbols(self, text: str) -> List[str]:
        """Extract potential stock symbols from text"""
        # Simple pattern to find potential stock symbols
        potential_symbols = re.findall(r'\b[A-Z]{1,5}\b', text)
        
        # Common stock symbols
        known_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']
        
        return [symbol for symbol in potential_symbols if symbol in known_symbols]


class CustomQueryWorkflow:
    """Workflow for handling custom user queries"""
    
    def __init__(self):
        logger.info("Initializing Custom Query Workflow")
        self.agents = AgentFactory.create_all_agents()
    
    def process_query(self, query: str) -> str:
        """Process any custom investment-related query"""
        
        logger.info(f"Processing custom query: {query[:100]}...")
        
        # Determine which agents to use based on query content
        query_lower = query.lower()
        
        results = []
        
        # Financial analysis needed?
        if any(word in query_lower for word in ['financial', 'earnings', 'revenue', 'profit', 'valuation', 'metrics']):
            logger.info("Using Financial Agent")
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                for symbol in symbols[:2]:
                    # Debug tool data first
                    debug_data = self.agents["financial"].debug_tool_data(symbol)
                    logger.info(f"DEBUG: Tool data for {symbol} in custom query: current_price = {debug_data.get('current_price')}")
                    
                    result = self.agents["financial"].analyze_stock(symbol)
                    
                    # Check for $1 in result
                    if isinstance(result, str) and "$1" in result:
                        logger.warning(f"WARNING: $1 detected in custom query financial analysis for {symbol}")
                    
                    results.append(f"Financial Analysis for {symbol}:\n{result}")
        
        # Technical analysis needed?
        if any(word in query_lower for word in ['technical', 'chart', 'trend', 'rsi', 'moving average', 'support', 'resistance']):
            logger.info("Using Technical Agent")
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                result = self.agents["technical"].technical_analysis(symbols[0])
                results.append(f"Technical Analysis:\n{result}")
        
        # News research needed?
        if any(word in query_lower for word in ['news', 'sentiment', 'market', 'trend', 'recent', 'latest']):
            logger.info("Using Research Agent")
            result = self.agents["research"].analyze_market_sentiment(query)
            results.append(f"Market Research:\n{result}")
        
        # Competitive analysis needed?
        if any(word in query_lower for word in ['competitor', 'compare', 'versus', 'vs', 'competition']):
            logger.info("Using Competitive Agent")
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                result = self.agents["competitive"].analyze_competitive_landscape(symbols[0])
                results.append(f"Competitive Analysis:\n{result}")
        
        # If no specific analysis detected, use research agent
        if not results:
            logger.info("Using general research")
            result = self.agents["research"].analyze_market_sentiment(query)
            results.append(result)
        
        # Combine all results
        combined_results = "\n\n---\n\n".join(results)
        
        # Generate final synthesis
        logger.info("Generating final response")
        final_response = self.agents["report"].create_market_summary({
            "query": query,
            "analysis_results": combined_results,
            "analysis_type": "custom_query",
            "timestamp": datetime.now().isoformat()
        })
        
        # Debug: Check final response
        logger.info(f"DEBUG: Custom query final response type: {type(final_response)}")
        
        # Check for $1 in final response
        if isinstance(final_response, str) and "$1" in final_response:
            logger.warning(f"WARNING: $1 detected in custom query final response")
        
        logger.info("Query processing complete")
        
        return final_response
    
    def _extract_symbols_from_query(self, query: str) -> List[str]:
        """Extract stock symbols from user query"""
        
        # Look for patterns like $AAPL, AAPL, etc.
        patterns = [
            r'\$([A-Z]{1,5})\b',
            r'\b([A-Z]{2,5})\b'
        ]
        
        symbols = []
        for pattern in patterns:
            matches = re.findall(pattern, query.upper())
            symbols.extend(matches)
        
        # Filter to known symbols
        known_symbols = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC', 'CRM', 'ORCL']
        
        return [symbol for symbol in symbols if symbol in known_symbols]


class WorkflowFactory:
    """Factory to create different types of workflows"""
    
    @staticmethod
    def create_investment_workflow():
        return InvestmentAnalysisWorkflow()
    
    @staticmethod
    def create_comparison_workflow():
        return ComparisonWorkflow()
    
    @staticmethod
    def create_research_workflow():
        return MarketResearchWorkflow()
    
    @staticmethod
    def create_custom_workflow():
        return CustomQueryWorkflow()