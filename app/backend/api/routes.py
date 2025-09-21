from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest
import logging
import traceback
from datetime import datetime
import threading
import uuid
from io import BytesIO

from workflows import WorkflowFactory
from tools import PDFGenerationTool

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Store for tracking analysis status
analysis_status = {}

@api_bp.route('/analyze/stock', methods=['POST'])
def analyze_stock():
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data:
            raise BadRequest("Symbol is required")
        
        symbol = data['symbol'].upper().strip()
        analysis_type = data.get('type', 'quick')
        
        if not symbol or len(symbol) > 5:
            raise BadRequest("Invalid symbol format")
        
        logger.info(f"Starting {analysis_type} analysis for {symbol}")
        
        if analysis_type == 'quick':
            workflow = WorkflowFactory.create_investment_workflow()
            result = workflow.quick_analysis(symbol)
            
            response = {
                "symbol": symbol,
                "analysis_type": "quick",
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
        else:
            workflow = WorkflowFactory.create_investment_workflow()
            result = workflow.analyze_stock(symbol)
            
            response = {
                "symbol": symbol,
                "analysis_type": "comprehensive",
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
        
        logger.info(f"Analysis completed for {symbol}")
        return jsonify(response)
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Analysis failed", "details": str(e)}), 500

@api_bp.route('/analyze/comparison', methods=['POST'])
def compare_stocks():
    try:
        data = request.get_json()
        
        if not data or 'symbols' not in data:
            raise BadRequest("Symbols list is required")
        
        symbols = [s.upper().strip() for s in data['symbols'] if s.strip()]
        
        if len(symbols) < 2:
            raise BadRequest("At least 2 symbols required for comparison")
        
        if len(symbols) > 5:
            raise BadRequest("Maximum 5 symbols allowed for comparison")
        
        logger.info(f"Starting comparison analysis for {symbols}")
        
        workflow = WorkflowFactory.create_comparison_workflow()
        result = workflow.compare_stocks(symbols)
        
        response = {
            "symbols": symbols,
            "analysis_type": "comparison",
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        logger.info(f"Comparison completed for {symbols}")
        return jsonify(response)
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Comparison failed", "details": str(e)}), 500

@api_bp.route('/analyze/research', methods=['POST'])
def market_research():
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            raise BadRequest("Research topic is required")
        
        topic = data['topic'].strip()
        
        if not topic:
            raise BadRequest("Topic cannot be empty")
        
        logger.info(f"Starting market research for: {topic}")
        
        workflow = WorkflowFactory.create_research_workflow()
        result = workflow.research_market_topic(topic)
        
        # Ensure we're returning the right structure
        if isinstance(result, dict) and 'research_report' in result:
            final_result = result['research_report']
        elif isinstance(result, dict):
            final_result = result
        else:
            final_result = str(result)
        
        response = {
            "topic": topic,
            "analysis_type": "market_research",
            "result": final_result,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        logger.info(f"Market research completed for: {topic}")
        return jsonify(response)
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Market research failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Market research failed", "details": str(e)}), 500

@api_bp.route('/analyze/query', methods=['POST'])
def custom_query():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            raise BadRequest("Query is required")
        
        query = data['query'].strip()
        
        if not query:
            raise BadRequest("Query cannot be empty")
        
        logger.info(f"Processing custom query: {query[:100]}...")
        
        workflow = WorkflowFactory.create_custom_workflow()
        result = workflow.process_query(query)
        
        response = {
            "query": query,
            "analysis_type": "custom_query",
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        logger.info("Custom query processing completed")
        return jsonify(response)
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Custom query failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Custom query failed", "details": str(e)}), 500

@api_bp.route('/download/pdf', methods=['POST'])
def download_pdf():
    try:
        data = request.get_json()
        
        if not data or 'content' not in data or 'title' not in data:
            raise BadRequest("Content and title are required")
        
        content = data['content']
        title = data['title']
        
        if not content or not title:
            raise BadRequest("Content and title cannot be empty")
        
        logger.info(f"Generating PDF for: {title}")
        
        # Extract content based on type
        markdown_content = ""
        
        if isinstance(content, dict):
            if content.get('analysis_type') == 'comprehensive':
                result = content.get('result', {})
                # Combine all comprehensive analysis sections
                sections = []
                if result.get('final_report'):
                    sections.append("# Final Report\n" + result.get('final_report'))
                if result.get('financial_analysis'):
                    sections.append("# Financial Analysis\n" + result.get('financial_analysis'))
                if result.get('technical_analysis'):
                    sections.append("# Technical Analysis\n" + result.get('technical_analysis'))
                if result.get('news_analysis'):
                    sections.append("# News Analysis\n" + result.get('news_analysis'))
                if result.get('competitive_analysis'):
                    sections.append("# Competitive Analysis\n" + result.get('competitive_analysis'))
                
                markdown_content = "\n\n---\n\n".join(sections)
                
            elif content.get('analysis_type') == 'market_research':
                result = content.get('result', {})
                if isinstance(result, dict):
                    markdown_content = result.get('research_report', '')
                else:
                    markdown_content = str(result)
                    
            elif content.get('analysis_type') == 'comparison':
                result = content.get('result', {})
                # Combine all comparison sections
                sections = []
                
                if result.get('comparison_report'):
                    sections.append("# Comparison Report\n" + result.get('comparison_report'))
                    
                if result.get('financial_comparison'):
                    sections.append("# Financial Comparison\n" + result.get('financial_comparison'))
                    
                if result.get('technical_comparison'):
                    sections.append("# Technical Comparison\n" + result.get('technical_comparison'))
                    
                if result.get('competitive_analyses'):
                    sections.append("# Competitive Analysis")
                    competitive_analyses = result.get('competitive_analyses', {})
                    for symbol, analysis in competitive_analyses.items():
                        sections.append(f"## {symbol} Competitive Analysis\n{analysis}")
                
                markdown_content = "\n\n---\n\n".join(sections)
                
            else:
                markdown_content = content.get('result', '')
        else:
            markdown_content = str(content)
        
        if not markdown_content:
            raise BadRequest("No content available for PDF generation")
        
        # Generate PDF
        pdf_tool = PDFGenerationTool()
        pdf_bytes = pdf_tool.generate_pdf(markdown_content, title)
        
        # Create BytesIO object for sending file
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        # Generate filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        logger.info(f"PDF generated successfully: {filename}")
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "PDF generation failed", "details": str(e)}), 500

@api_bp.route('/analyze/async/stock', methods=['POST'])
def analyze_stock_async():
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data:
            raise BadRequest("Symbol is required")
        
        symbol = data['symbol'].upper().strip()
        analysis_type = data.get('type', 'comprehensive')
        
        if not symbol or len(symbol) > 5:
            raise BadRequest("Invalid symbol format")
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Initialize status
        analysis_status[task_id] = {
            "status": "started",
            "symbol": symbol,
            "analysis_type": analysis_type,
            "started_at": datetime.now().isoformat(),
            "progress": 0
        }
        
        # Start analysis in background thread
        def run_analysis():
            try:
                logger.info(f"Starting async {analysis_type} analysis for {symbol}")
                
                analysis_status[task_id]["status"] = "processing"
                analysis_status[task_id]["progress"] = 25
                
                workflow = WorkflowFactory.create_investment_workflow()
                
                if analysis_type == 'quick':
                    result = workflow.quick_analysis(symbol)
                else:
                    result = workflow.analyze_stock(symbol)
                
                analysis_status[task_id].update({
                    "status": "completed",
                    "progress": 100,
                    "result": result,
                    "completed_at": datetime.now().isoformat()
                })
                
                logger.info(f"Async analysis completed for {symbol}")
                
            except Exception as e:
                logger.error(f"Async analysis failed for {symbol}: {e}")
                analysis_status[task_id].update({
                    "status": "failed",
                    "error": str(e),
                    "failed_at": datetime.now().isoformat()
                })
        
        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "task_id": task_id,
            "status": "started",
            "message": f"Analysis started for {symbol}"
        })
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Failed to start async analysis: {e}")
        return jsonify({"error": "Failed to start analysis", "details": str(e)}), 500

@api_bp.route('/status/<task_id>', methods=['GET'])
def get_analysis_status(task_id):
    try:
        if task_id not in analysis_status:
            return jsonify({"error": "Task not found"}), 404
        
        status_data = analysis_status[task_id].copy()
        
        # Clean up completed/failed tasks after 1 hour
        if status_data.get("status") in ["completed", "failed"]:
            completed_time = status_data.get("completed_at") or status_data.get("failed_at")
            if completed_time:
                from datetime import datetime, timedelta
                completed_dt = datetime.fromisoformat(completed_time)
                if datetime.now() - completed_dt > timedelta(hours=1):
                    del analysis_status[task_id]
        
        return jsonify(status_data)
        
    except Exception as e:
        logger.error(f"Failed to get status for task {task_id}: {e}")
        return jsonify({"error": "Failed to get status"}), 500

@api_bp.route('/validate/symbol/<symbol>', methods=['GET'])
def validate_symbol(symbol):
    try:
        symbol = symbol.upper().strip()
        
        # Basic validation
        if not symbol or len(symbol) > 5 or not symbol.isalpha():
            return jsonify({"valid": False, "reason": "Invalid format"})
        
        # Try to fetch basic data to verify symbol exists
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if info.get("symbol") == symbol or info.get("shortName"):
            return jsonify({
                "valid": True,
                "symbol": symbol,
                "name": info.get("shortName", "Unknown"),
                "sector": info.get("sector"),
                "industry": info.get("industry")
            })
        else:
            return jsonify({"valid": False, "reason": "Symbol not found"})
            
    except Exception as e:
        logger.warning(f"Symbol validation failed for {symbol}: {e}")
        return jsonify({"valid": False, "reason": "Validation failed"})

@api_bp.route('/system/info', methods=['GET'])
def system_info():
    return jsonify({
        "service": "IntelliMarket API",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Single stock analysis",
            "Stock comparison",
            "Market research", 
            "Custom queries",
            "Async processing",
            "PDF report generation"
        ],
        "timestamp": datetime.now().isoformat()
    })