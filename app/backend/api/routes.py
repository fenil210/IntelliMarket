from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import logging
import traceback
from datetime import datetime
import threading
import uuid

from workflows import WorkflowFactory

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
            "Async processing"
        ],
        "timestamp": datetime.now().isoformat()
    })