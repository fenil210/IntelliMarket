import yfinance as yf
import requests
from duckduckgo_search import DDGS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import logging
from typing import Dict, List, Any, Optional
from agno.tools import Toolkit
from pydantic import BaseModel, Field
import markdown
from io import BytesIO
import tempfile
import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

logger = logging.getLogger(__name__)


class FinancialDataTool(Toolkit):
    """Tool for fetching financial data using YFinance"""
    
    def _format_large_number(self, number):
        """Format large numbers into readable format (e.g., 1.5T, 500.2B, 10.3M)"""
        if not number or number == 0:
            return "N/A"
        
        try:
            number = float(number)
            
            if number >= 1e12:
                return f"${number/1e12:.1f}T"
            elif number >= 1e9:
                return f"${number/1e9:.1f}B"
            elif number >= 1e6:
                return f"${number/1e6:.1f}M"
            elif number >= 1e3:
                return f"${number/1e3:.1f}K"
            else:
                return f"${number:.2f}"
        except (ValueError, TypeError):
            return "N/A"
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Get stock price data and basic info"""
        try:
            logger.info(f"Fetching stock data for {symbol}")
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            
            # Get stock info
            info = ticker.info
            
            if hist.empty:
                logger.warning(f"No historical data available for {symbol}")
                return {"error": f"No historical data available for {symbol}"}
            
            # Calculate basic metrics
            current_price = hist['Close'].iloc[-1] if len(hist) > 0 else None
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2] if len(hist) > 1 else 0
            price_change_pct = (price_change / hist['Close'].iloc[-2]) * 100 if len(hist) > 1 else 0
            
            # Format market cap properly
            market_cap = info.get("marketCap") or info.get("marketCapitalization")
            market_cap_formatted = self._format_large_number(market_cap) if market_cap else "N/A"
            
            # Format other financial metrics
            pe_ratio = info.get("trailingPE") or info.get("forwardPE")
            eps = info.get("trailingEps") or info.get("forwardEps")
            
            # Format revenue
            revenue = info.get("totalRevenue") or info.get("revenue")
            revenue_formatted = self._format_large_number(revenue) if revenue else "N/A"
            
            # Format enterprise value
            enterprise_value = info.get("enterpriseValue")
            enterprise_value_formatted = self._format_large_number(enterprise_value) if enterprise_value else "N/A"
            
            result = {
                "symbol": symbol,
                "current_price": round(current_price, 2) if current_price else None,
                "price_change": round(price_change, 2),
                "price_change_pct": round(price_change_pct, 2),
                "market_cap": market_cap,
                "market_cap_formatted": market_cap_formatted,
                "pe_ratio": round(pe_ratio, 2) if pe_ratio else None,
                "eps": round(eps, 2) if eps else None,
                "dividend_yield": round(info.get("dividendYield") * 100, 2) if info.get("dividendYield") else None,
                "52_week_high": round(info.get("fiftyTwoWeekHigh"), 2) if info.get("fiftyTwoWeekHigh") else None,
                "52_week_low": round(info.get("fiftyTwoWeekLow"), 2) if info.get("fiftyTwoWeekLow") else None,
                "volume": int(hist['Volume'].iloc[-1]) if len(hist) > 0 else None,
                "avg_volume": int(info.get("averageVolume")) if info.get("averageVolume") else None,
                "sector": info.get("sector") or "N/A",
                "industry": info.get("industry") or "N/A",
                "business_summary": info.get("longBusinessSummary", "")[:500],
                # Additional financial metrics with proper formatting
                "revenue": revenue,
                "revenue_formatted": revenue_formatted,
                "gross_margin": round(info.get("grossMargins") * 100, 2) if info.get("grossMargins") else None,
                "operating_margin": round(info.get("operatingMargins") * 100, 2) if info.get("operatingMargins") else None,
                "profit_margin": round(info.get("profitMargins") * 100, 2) if info.get("profitMargins") else None,
                "roe": round(info.get("returnOnEquity") * 100, 2) if info.get("returnOnEquity") else None,
                "debt_to_equity": round(info.get("debtToEquity"), 2) if info.get("debtToEquity") else None,
                "current_ratio": round(info.get("currentRatio"), 2) if info.get("currentRatio") else None,
                "book_value": round(info.get("bookValue"), 2) if info.get("bookValue") else None,
                "enterprise_value": enterprise_value,
                "enterprise_value_formatted": enterprise_value_formatted
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
    
    def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements"""
        try:
            logger.info(f"Fetching financial statements for {symbol}")
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
            logger.error(f"Failed to fetch financial statements for {symbol}: {e}")
            return {"error": f"Failed to fetch financial statements for {symbol}: {str(e)}"}
    
    def calculate_technical_indicators(self, symbol: str, period: str = "6mo") -> Dict[str, Any]:
        """Calculate basic technical indicators"""
        try:
            logger.info(f"Calculating technical indicators for {symbol}")
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
            logger.error(f"Failed to calculate technical indicators for {symbol}: {e}")
            return {"error": f"Failed to calculate technical indicators for {symbol}: {str(e)}"}


class WebResearchTool(Toolkit):
    """Tool for web research using DuckDuckGo"""
    
    def search_news(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for news articles"""
        try:
            logger.info(f"Searching news for: {query}")
            with DDGS() as ddgs:
                results = []
                for result in ddgs.news(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "source": result.get("source", ""),
                        "date": result.get("date", ""),
                        "body": result.get("body", "")[:300]
                    })
                logger.info(f"Found {len(results)} news articles")
                return results
        except Exception as e:
            logger.error(f"News search failed for {query}: {e}")
            return [{"error": f"Search failed: {str(e)}"}]
    
    def search_general(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """General web search"""
        try:
            logger.info(f"Performing general search for: {query}")
            with DDGS() as ddgs:
                results = []
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")[:300]
                    })
                logger.info(f"Found {len(results)} search results")
                return results
        except Exception as e:
            logger.error(f"General search failed for {query}: {e}")
            return [{"error": f"Search failed: {str(e)}"}]


class CompetitiveAnalysisTool(Toolkit):
    """Tool for competitive analysis"""
    
    def compare_companies(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple companies"""
        logger.info(f"Comparing companies: {symbols}")
        comparison_data = {}
        financial_tool = FinancialDataTool()
        
        for symbol in symbols:
            data = financial_tool.get_stock_data(symbol)
            if "error" not in data:
                comparison_data[symbol] = {
                    "current_price": data.get("current_price"),
                    "market_cap": data.get("market_cap_formatted"),
                    "pe_ratio": data.get("pe_ratio"),
                    "price_change_pct": data.get("price_change_pct"),
                    "sector": data.get("sector"),
                    "industry": data.get("industry"),
                    "revenue": data.get("revenue_formatted"),
                    "gross_margin": data.get("gross_margin"),
                    "operating_margin": data.get("operating_margin"),
                    "roe": data.get("roe")
                }
        
        return {
            "comparison_data": comparison_data,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def get_sector_peers(self, symbol: str) -> List[str]:
        """Get sector peers for a given stock"""
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
            logger.info(f"Creating price chart for {symbol}")
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
            logger.error(f"Chart generation failed for {symbol}: {e}")
            return f"Chart generation failed: {str(e)}"
    
    def create_comparison_chart(self, symbols: List[str], period: str = "6mo") -> str:
        """Create a comparison chart for multiple stocks"""
        try:
            logger.info(f"Creating comparison chart for {symbols}")
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
            logger.error(f"Comparison chart generation failed: {e}")
            return f"Comparison chart generation failed: {str(e)}"


class PDFGenerationTool(Toolkit):
    """Tool for generating PDF reports from markdown content using ReportLab"""
    
    def __init__(self):
        self.styles = self._create_styles()
    
    def _create_styles(self):
        """Create custom paragraph styles for the PDF"""
        styles = getSampleStyleSheet()
        
        # Custom styles for financial reports with unique names
        styles.add(ParagraphStyle(
            name='IntelliReportTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#667eea'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliReportSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=HexColor('#718096'),
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliHeading1',
            parent=styles['Normal'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=24,
            textColor=HexColor('#1a202c'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliHeading2',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica-Bold',
            leftIndent=10
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliHeading3',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliBodyText',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=HexColor('#4a5568'),
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='IntelliBulletText',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            leftIndent=20,
            bulletIndent=10,
            textColor=HexColor('#4a5568'),
            fontName='Helvetica'
        ))
        
        return styles
    
    def generate_pdf(self, content: str, title: str) -> bytes:
        """Generate PDF from markdown content"""
        try:
            logger.info(f"Generating PDF report: {title}")
            
            # Create PDF buffer
            buffer = BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Parse markdown content
            story = self._parse_markdown_to_story(content, title)
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(f"PDF generated successfully, size: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def _parse_markdown_to_story(self, content: str, title: str) -> List:
        """Convert markdown content to ReportLab story elements"""
        story = []
        
        # Add title page
        story.append(Paragraph(title, self.styles['IntelliReportTitle']))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['IntelliReportSubtitle']))
        story.append(Spacer(1, 20))
        
        # Split content into lines
        lines = content.split('\n')
        current_list_items = []
        in_table = False
        table_data = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                # Add spacing for empty lines
                if current_list_items:
                    self._add_list_to_story(story, current_list_items)
                    current_list_items = []
                story.append(Spacer(1, 6))
                continue
            
            # Handle headers
            if line.startswith('#'):
                if current_list_items:
                    self._add_list_to_story(story, current_list_items)
                    current_list_items = []
                
                level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('#').strip()
                
                if level == 1:
                    story.append(Paragraph(self._format_text(header_text), self.styles['IntelliHeading1']))
                elif level == 2:
                    story.append(Paragraph(self._format_text(header_text), self.styles['IntelliHeading2']))
                else:
                    story.append(Paragraph(self._format_text(header_text), self.styles['IntelliHeading3']))
                continue
            
            # Handle bullet points
            if line.startswith(('- ', '* ')):
                list_text = line[2:].strip()
                current_list_items.append(list_text)
                continue
            
            # Handle tables
            if '|' in line and line.startswith('|') and line.endswith('|'):
                if not in_table:
                    in_table = True
                    table_data = []
                
                # Parse table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                
                # Skip separator rows
                if all(cell.replace('-', '').strip() == '' for cell in cells):
                    continue
                
                table_data.append(cells)
                continue
            else:
                # End of table
                if in_table:
                    self._add_table_to_story(story, table_data)
                    table_data = []
                    in_table = False
            
            # Handle regular paragraphs
            if current_list_items:
                self._add_list_to_story(story, current_list_items)
                current_list_items = []
            
            if line and not line.startswith('#'):
                story.append(Paragraph(self._format_text(line), self.styles['IntelliBodyText']))
        
        # Handle remaining items
        if current_list_items:
            self._add_list_to_story(story, current_list_items)
        
        if table_data:
            self._add_table_to_story(story, table_data)
        
        return story
    
    def _add_list_to_story(self, story: List, items: List[str]):
        """Add bullet list to story"""
        for item in items:
            story.append(Paragraph(f"• {self._format_text(item)}", self.styles['IntelliBulletText']))
    
    def _add_table_to_story(self, story: List, table_data: List[List[str]]):
        """Add table to story"""
        if not table_data:
            return
        
        # Format table data - don't apply HTML formatting to table cells
        formatted_data = []
        for row in table_data:
            formatted_row = [self._clean_text_for_table(cell) for cell in row]
            formatted_data.append(formatted_row)
        
        # Create table
        table = Table(formatted_data)
        
        # Basic table style without dynamic additions
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8fafc')])
        ])
        
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 12))
    
    def _clean_text_for_table(self, text: str) -> str:
        """Clean text for table cells - remove HTML and return plain text"""
        if not text:
            return ""
        
        # Remove any existing HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Handle bold and italic markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        
        return text.strip()
    
    def _is_financial_amount(self, text: str) -> bool:
        """Check if text is a financial amount"""
        return bool(re.match(r'^\$[0-9]+(?:\.[0-9]+)?[KMB]?$', text.strip()))
    
    def _is_percentage(self, text: str) -> bool:
        """Check if text is a percentage"""
        return bool(re.match(r'^[0-9]+(?:\.[0-9]+)?%$', text.strip()))
    
    def _is_stock_symbol(self, text: str) -> bool:
        """Check if text is a stock symbol"""
        return bool(re.match(r'^[A-Z]{2,5}$', text.strip()))
    
    def _format_text(self, text: str) -> str:
        """Format text with financial styling"""
        if not text:
            return ""
        
        # Handle bold text
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
        
        # Handle financial amounts
        text = re.sub(
            r'\$([0-9]+(?:\.[0-9]+)?[KMB]?)', 
            r'<font color="#38a169" face="Courier-Bold">$\1</font>', 
            text
        )
        
        # Handle percentages
        text = re.sub(
            r'([0-9]+(?:\.[0-9]+)?%)', 
            r'<font color="#3182ce" face="Courier-Bold">\1</font>', 
            text
        )
        
        # Handle stock symbols
        text = re.sub(
            r'\b([A-Z]{2,5})\b(?!\s*[a-z])', 
            r'<font color="#667eea" face="Courier-Bold">\1</font>', 
            text
        )
        
        return text


class ReportGenerationTool(Toolkit):
    """Tool for generating reports"""
    
    def generate_summary_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate a summary report from analysis data"""
        try:
            logger.info("Generating summary report")
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
            logger.error(f"Report generation failed: {e}")
            return f"Report generation failed: {str(e)}"
    
    def _format_financial_data(self, data: Dict) -> str:
        if not data or "error" in data:
            return "Financial data unavailable"
        
        current_price = data.get('current_price', 'N/A')
        price_change_pct = data.get('price_change_pct', 0)
        market_cap = data.get('market_cap_formatted', 'N/A')
        pe_ratio = data.get('pe_ratio', 'N/A')
        sector = data.get('sector', 'N/A')
        
        return f"""
- **Current Price:** ${current_price}
- **Price Change:** {price_change_pct:.2f}%
- **Market Cap:** {market_cap}
- **P/E Ratio:** {pe_ratio}
- **Sector:** {sector}
"""
    
    def _format_technical_data(self, data: Dict) -> str:
        if not data or "error" in data:
            return "Technical data unavailable"
        
        rsi = data.get('rsi', 'N/A')
        rsi_condition = data.get('trend_analysis', {}).get('rsi_condition', 'N/A')
        above_sma_20 = data.get('trend_analysis', {}).get('above_sma_20')
        above_sma_50 = data.get('trend_analysis', {}).get('above_sma_50')
        
        return f"""
- **RSI:** {rsi} ({rsi_condition})
- **Price vs SMA20:** {'Above' if above_sma_20 else 'Below'}
- **Price vs SMA50:** {'Above' if above_sma_50 else 'Below'}
"""
    
    def _format_news_data(self, data: List) -> str:
        if not data:
            return "No recent news available"
        
        news_summary = ""
        for item in data[:3]:
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
            current_price = metrics.get('current_price', 'N/A')
            price_change_pct = metrics.get('price_change_pct', 0)
            comp_summary += f"- **{symbol}:** ${current_price} ({price_change_pct:.2f}%)\n"
        
        return comp_summary.strip()