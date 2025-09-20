import yfinance as yf
import requests
from duckduckgo_search import DDGS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import Dict, List, Any, Optional
from agno.tools import Toolkit
from pydantic import BaseModel, Field


class FinancialDataTool(Toolkit):
    """Tool for fetching financial data using YFinance"""
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Get stock price data and basic info"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            
            # Get stock info
            info = ticker.info
            
            # Calculate basic metrics
            current_price = hist['Close'][-1] if len(hist) > 0 else None
            price_change = hist['Close'][-1] - hist['Close'][-2] if len(hist) > 1 else 0
            price_change_pct = (price_change / hist['Close'][-2]) * 100 if len(hist) > 1 else 0
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2) if current_price else None,
                "price_change": round(price_change, 2),
                "price_change_pct": round(price_change_pct, 2),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "eps": info.get("trailingEps"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "volume": hist['Volume'][-1] if len(hist) > 0 else None,
                "avg_volume": info.get("averageVolume"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "business_summary": info.get("longBusinessSummary", "")[:500]
            }
        except Exception as e:
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
    
    def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial statements
            income_stmt = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            return {
                "symbol": symbol,
                "income_statement": income_stmt.to_dict() if not income_stmt.empty else {},
                "balance_sheet": balance_sheet.to_dict() if not balance_sheet.empty else {},
                "cash_flow": cash_flow.to_dict() if not cash_flow.empty else {}
            }
        except Exception as e:
            return {"error": f"Failed to fetch financial statements for {symbol}: {str(e)}"}
    
    def calculate_technical_indicators(self, symbol: str, period: str = "6mo") -> Dict[str, Any]:
        """Calculate basic technical indicators"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": "No data available"}
            
            # Simple Moving Averages
            sma_20 = hist['Close'].rolling(window=20).mean()
            sma_50 = hist['Close'].rolling(window=50).mean()
            
            # RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = hist['Close'].ewm(span=12).mean()
            exp2 = hist['Close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            
            current_price = hist['Close'][-1]
            current_sma_20 = sma_20[-1] if not sma_20.empty else None
            current_sma_50 = sma_50[-1] if not sma_50.empty else None
            current_rsi = rsi[-1] if not rsi.empty else None
            current_macd = macd[-1] if not macd.empty else None
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "sma_20": round(current_sma_20, 2) if current_sma_20 else None,
                "sma_50": round(current_sma_50, 2) if current_sma_50 else None,
                "rsi": round(current_rsi, 2) if current_rsi else None,
                "macd": round(current_macd, 2) if current_macd else None,
                "trend_analysis": {
                    "above_sma_20": current_price > current_sma_20 if current_sma_20 else None,
                    "above_sma_50": current_price > current_sma_50 if current_sma_50 else None,
                    "rsi_condition": "oversold" if current_rsi and current_rsi < 30 else "overbought" if current_rsi and current_rsi > 70 else "neutral"
                }
            }
        except Exception as e:
            return {"error": f"Failed to calculate technical indicators for {symbol}: {str(e)}"}


class WebResearchTool(Toolkit):
    """Tool for web research using DuckDuckGo"""
    
    def search_news(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for news articles"""
        try:
            with DDGS() as ddgs:
                results = []
                for result in ddgs.news(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "source": result.get("source", ""),
                        "date": result.get("date", ""),
                        "body": result.get("body", "")[:300]  # Truncate for brevity
                    })
                return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def search_general(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """General web search"""
        try:
            with DDGS() as ddgs:
                results = []
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")[:300]
                    })
                return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]


class CompetitiveAnalysisTool(Toolkit):
    """Tool for competitive analysis"""
    
    def compare_companies(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple companies"""
        comparison_data = {}
        financial_tool = FinancialDataTool()
        
        for symbol in symbols:
            data = financial_tool.get_stock_data(symbol)
            if "error" not in data:
                comparison_data[symbol] = {
                    "current_price": data.get("current_price"),
                    "market_cap": data.get("market_cap"),
                    "pe_ratio": data.get("pe_ratio"),
                    "price_change_pct": data.get("price_change_pct"),
                    "sector": data.get("sector"),
                    "industry": data.get("industry")
                }
        
        return {
            "comparison_data": comparison_data,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def get_sector_peers(self, symbol: str) -> List[str]:
        """Get sector peers for a given stock (simplified)"""
        # This is a simplified version - in production, you'd use a proper API
        sector_peers = {
            "AAPL": ["MSFT", "GOOGL", "META", "AMZN"],
            "TSLA": ["GM", "F", "RIVN", "LCID"],
            "NVDA": ["AMD", "INTC", "QCOM", "AVGO"],
            "MSFT": ["AAPL", "GOOGL", "META", "AMZN"],
            "GOOGL": ["AAPL", "MSFT", "META", "AMZN"]
        }
        return sector_peers.get(symbol.upper(), [])


class ChartGenerationTool(Toolkit):
    """Tool for generating charts and visualizations"""
    
    def create_price_chart(self, symbol: str, period: str = "6mo") -> str:
        """Create a price chart for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return "No data available for chart generation"
            
            fig = go.Figure()
            
            # Add candlestick chart
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=symbol
            ))
            
            fig.update_layout(
                title=f"{symbol} Stock Price ({period})",
                yaxis_title="Price ($)",
                xaxis_title="Date",
                template="plotly_white"
            )
            
            return fig.to_html(include_plotlyjs='cdn')
        except Exception as e:
            return f"Chart generation failed: {str(e)}"
    
    def create_comparison_chart(self, symbols: List[str], period: str = "6mo") -> str:
        """Create a comparison chart for multiple stocks"""
        try:
            fig = go.Figure()
            
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                
                if not hist.empty:
                    # Normalize to percentage change
                    normalized = (hist['Close'] / hist['Close'].iloc[0] - 1) * 100
                    
                    fig.add_trace(go.Scatter(
                        x=hist.index,
                        y=normalized,
                        mode='lines',
                        name=symbol,
                        line=dict(width=2)
                    ))
            
            fig.update_layout(
                title=f"Stock Price Comparison ({period})",
                yaxis_title="Percentage Change (%)",
                xaxis_title="Date",
                template="plotly_white",
                legend=dict(x=0, y=1)
            )
            
            return fig.to_html(include_plotlyjs='cdn')
        except Exception as e:
            return f"Comparison chart generation failed: {str(e)}"


class ReportGenerationTool(Toolkit):
    """Tool for generating reports"""
    
    def generate_summary_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate a summary report from analysis data"""
        try:
            report = f"""
# Investment Analysis Report
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
{analysis_data.get('executive_summary', 'Analysis completed')}

## Financial Metrics
{self._format_financial_data(analysis_data.get('financial_data', {}))}

## Technical Analysis
{self._format_technical_data(analysis_data.get('technical_data', {}))}

## Market News & Sentiment
{self._format_news_data(analysis_data.get('news_data', []))}

## Competitive Position
{self._format_competitive_data(analysis_data.get('competitive_data', {}))}

## Recommendation
{analysis_data.get('recommendation', 'Further analysis required')}
"""
            return report
        except Exception as e:
            return f"Report generation failed: {str(e)}"
    
    def _format_financial_data(self, data: Dict) -> str:
        if not data or "error" in data:
            return "Financial data unavailable"
        
        return f"""
- **Current Price:** ${data.get('current_price', 'N/A')}
- **Price Change:** {data.get('price_change_pct', 0):.2f}%
- **Market Cap:** ${data.get('market_cap', 'N/A'):,} (if available)
- **P/E Ratio:** {data.get('pe_ratio', 'N/A')}
- **Sector:** {data.get('sector', 'N/A')}
"""
    
    def _format_technical_data(self, data: Dict) -> str:
        if not data or "error" in data:
            return "Technical data unavailable"
        
        return f"""
- **RSI:** {data.get('rsi', 'N/A')} ({data.get('trend_analysis', {}).get('rsi_condition', 'N/A')})
- **Price vs SMA20:** {'Above' if data.get('trend_analysis', {}).get('above_sma_20') else 'Below'}
- **Price vs SMA50:** {'Above' if data.get('trend_analysis', {}).get('above_sma_50') else 'Below'}
"""
    
    def _format_news_data(self, data: List) -> str:
        if not data:
            return "No recent news available"
        
        news_summary = ""
        for item in data[:3]:  # Top 3 news items
            if "error" not in item:
                news_summary += f"- **{item.get('title', 'N/A')}** ({item.get('source', 'Unknown')})\n"
        
        return news_summary or "No recent news available"
    
    def _format_competitive_data(self, data: Dict) -> str:
        if not data or "error" in data:
            return "Competitive data unavailable"
        
        comparison = data.get('comparison_data', {})
        if not comparison:
            return "No comparison data available"
        
        comp_summary = ""
        for symbol, metrics in comparison.items():
            comp_summary += f"- **{symbol}:** ${metrics.get('current_price', 'N/A')} ({metrics.get('price_change_pct', 0):.2f}%)\n"
        
        return comp_summary