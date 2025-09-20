from typing import Dict, List, Any
from agents import AgentFactory
from datetime import datetime
import json


class InvestmentAnalysisWorkflow:
    """Workflow for comprehensive investment analysis"""
    
    def __init__(self):
        self.agents = AgentFactory.create_all_agents()
        self.results = {}
    
    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Complete stock analysis workflow"""
        
        print(f"🔍 Starting comprehensive analysis for {symbol}...")
        
        # Step 1: Financial Analysis
        print("📊 Performing financial analysis...")
        financial_analysis = self.agents["financial"].analyze_stock(symbol)
        self.results["financial"] = financial_analysis
        
        # Step 2: Technical Analysis  
        print("📈 Performing technical analysis...")
        technical_analysis = self.agents["technical"].technical_analysis(symbol)
        self.results["technical"] = technical_analysis
        
        # Step 3: News Research
        print("📰 Researching company news...")
        news_analysis = self.agents["research"].research_company_news(symbol)
        self.results["news"] = news_analysis
        
        # Step 4: Competitive Analysis
        print("🏢 Analyzing competitive landscape...")
        competitive_analysis = self.agents["competitive"].analyze_competitive_landscape(symbol)
        self.results["competitive"] = competitive_analysis
        
        # Step 5: Generate Final Report
        print("📝 Generating comprehensive report...")
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
        self.results["final_report"] = final_report
        
        print("✅ Analysis complete!")
        
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
        print(f"⚡ Quick analysis for {symbol}...")
        
        # Just financial and technical analysis
        financial = self.agents["financial"].analyze_stock(symbol)
        technical = self.agents["technical"].technical_analysis(symbol)
        
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
        
        return report


class ComparisonWorkflow:
    """Workflow for comparing multiple stocks"""
    
    def __init__(self):
        self.agents = AgentFactory.create_all_agents()
    
    def compare_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple stocks across different dimensions"""
        
        print(f"🔄 Comparing stocks: {', '.join(symbols)}...")
        
        results = {}
        
        # Financial Comparison
        print("📊 Financial comparison...")
        financial_comparison = self.agents["financial"].compare_stocks(symbols)
        results["financial_comparison"] = financial_comparison
        
        # Technical Comparison
        print("📈 Technical comparison...")
        technical_comparison = self.agents["technical"].chart_analysis(symbols)
        results["technical_comparison"] = technical_comparison
        
        # Competitive Analysis for each stock
        print("🏢 Competitive analysis...")
        competitive_analyses = {}
        for symbol in symbols:
            competitive_analyses[symbol] = self.agents["competitive"].analyze_competitive_landscape(symbol)
        results["competitive_analyses"] = competitive_analyses
        
        # Generate comparison report
        print("📝 Generating comparison report...")
        comparison_report = self.agents["report"].create_market_summary({
            "symbols": symbols,
            "financial_comparison": financial_comparison,
            "technical_comparison": technical_comparison,
            "competitive_analyses": competitive_analyses,
            "analysis_type": "comparison",
            "timestamp": datetime.now().isoformat()
        })
        results["comparison_report"] = comparison_report
        
        print("✅ Comparison complete!")
        
        return results


class MarketResearchWorkflow:
    """Workflow for market research and sentiment analysis"""
    
    def __init__(self):
        self.agents = AgentFactory.create_all_agents()
    
    def research_market_topic(self, topic: str) -> Dict[str, Any]:
        """Research a specific market topic or trend"""
        
        print(f"🔬 Researching market topic: {topic}...")
        
        results = {}
        
        # Web research for the topic
        print("🌐 Web research...")
        web_research = self.agents["research"].analyze_market_sentiment(topic)
        results["web_research"] = web_research
        
        # If topic contains stock symbols, analyze them
        potential_symbols = self._extract_symbols(topic)
        if potential_symbols:
            print(f"📊 Found potential stocks: {potential_symbols}")
            financial_context = {}
            for symbol in potential_symbols[:3]:  # Limit to 3 stocks
                financial_context[symbol] = self.agents["financial"].analyze_stock(symbol)
            results["financial_context"] = financial_context
        
        # Generate research report
        print("📝 Generating research report...")
        research_report = self.agents["report"].create_market_summary({
            "topic": topic,
            "web_research": web_research,
            "financial_context": results.get("financial_context", {}),
            "analysis_type": "market_research",
            "timestamp": datetime.now().isoformat()
        })
        results["research_report"] = research_report
        
        print("✅ Market research complete!")
        
        return results
    
    def _extract_symbols(self, text: str) -> List[str]:
        """Extract potential stock symbols from text"""
        import re
        # Simple pattern to find potential stock symbols
        potential_symbols = re.findall(r'\b[A-Z]{1,5}\b', text)
        
        # Common stock symbols (you could expand this)
        known_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']
        
        return [symbol for symbol in potential_symbols if symbol in known_symbols]


class CustomQueryWorkflow:
    """Workflow for handling custom user queries"""
    
    def __init__(self):
        self.agents = AgentFactory.create_all_agents()
    
    def process_query(self, query: str) -> str:
        """Process any custom investment-related query"""
        
        print(f"🤔 Processing query: {query[:50]}...")
        
        # Determine which agents to use based on query content
        query_lower = query.lower()
        
        results = []
        
        # Financial analysis needed?
        if any(word in query_lower for word in ['financial', 'earnings', 'revenue', 'profit', 'valuation', 'metrics']):
            print("📊 Using Financial Agent...")
            # Extract any stock symbols mentioned
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                for symbol in symbols[:2]:  # Limit to 2 stocks
                    result = self.agents["financial"].analyze_stock(symbol)
                    results.append(f"Financial Analysis for {symbol}:\n{result}")
        
        # Technical analysis needed?
        if any(word in query_lower for word in ['technical', 'chart', 'trend', 'rsi', 'moving average', 'support', 'resistance']):
            print("📈 Using Technical Agent...")
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                result = self.agents["technical"].technical_analysis(symbols[0])
                results.append(f"Technical Analysis:\n{result}")
        
        # News research needed?
        if any(word in query_lower for word in ['news', 'sentiment', 'market', 'trend', 'recent', 'latest']):
            print("📰 Using Research Agent...")
            result = self.agents["research"].analyze_market_sentiment(query)
            results.append(f"Market Research:\n{result}")
        
        # Competitive analysis needed?
        if any(word in query_lower for word in ['competitor', 'compare', 'versus', 'vs', 'competition']):
            print("🏢 Using Competitive Agent...")
            symbols = self._extract_symbols_from_query(query)
            if symbols:
                result = self.agents["competitive"].analyze_competitive_landscape(symbols[0])
                results.append(f"Competitive Analysis:\n{result}")
        
        # If no specific analysis detected, use research agent
        if not results:
            print("🔍 Using general research...")
            result = self.agents["research"].analyze_market_sentiment(query)
            results.append(result)
        
        # Combine all results
        combined_results = "\n\n---\n\n".join(results)
        
        # Generate final synthesis
        print("📝 Generating final response...")
        final_response = self.agents["report"].create_market_summary({
            "query": query,
            "analysis_results": combined_results,
            "analysis_type": "custom_query",
            "timestamp": datetime.now().isoformat()
        })
        
        print("✅ Query processing complete!")
        
        return final_response
    
    def _extract_symbols_from_query(self, query: str) -> List[str]:
        """Extract stock symbols from user query"""
        import re
        
        # Look for patterns like $AAPL, AAPL, etc.
        patterns = [
            r'\$([A-Z]{1,5})\b',  # $AAPL format
            r'\b([A-Z]{2,5})\b'   # AAPL format
        ]
        
        symbols = []
        for pattern in patterns:
            matches = re.findall(pattern, query.upper())
            symbols.extend(matches)
        
        # Filter to known symbols
        known_symbols = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC', 'CRM', 'ORCL']
        
        return [symbol for symbol in symbols if symbol in known_symbols]


# Workflow Factory
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