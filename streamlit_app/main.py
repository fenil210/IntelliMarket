import streamlit as st
import time
from datetime import datetime
from config import Config
from workflows import WorkflowFactory
import traceback


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title=Config.PAGE_TITLE,
        page_icon=Config.PAGE_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please check your .env file and ensure GOOGLE_API_KEY is set correctly.")
        st.stop()
    
    # App header
    st.title("📊 IntelliMarket Research Platform")
    st.markdown("*AI-Powered Investment Analysis and Market Research*")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Analysis Options")
        
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            [
                "🏢 Single Stock Analysis",
                "⚖️ Stock Comparison", 
                "🌐 Market Research",
                "❓ Custom Query"
            ]
        )
        
        st.divider()
        
        # Analysis speed
        analysis_speed = st.radio(
            "Analysis Depth:",
            ["⚡ Quick Analysis", "🔍 Comprehensive Analysis"],
            help="Quick analysis is faster but less detailed"
        )
        
        st.divider()
        
        # System status
        st.header("📡 System Status")
        st.success("✅ Gemini API Connected")
        st.info(f"🤖 Model: {Config.GEMINI_MODEL}")
        st.info(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content area
    if analysis_type == "🏢 Single Stock Analysis":
        single_stock_analysis(analysis_speed)
    
    elif analysis_type == "⚖️ Stock Comparison":
        stock_comparison_analysis()
        
    elif analysis_type == "🌐 Market Research":
        market_research_analysis()
        
    elif analysis_type == "❓ Custom Query":
        custom_query_analysis()


def single_stock_analysis(analysis_speed):
    """Single stock analysis interface"""
    
    st.header("🏢 Single Stock Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        symbol = st.text_input(
            "Enter Stock Symbol:",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter a valid stock ticker symbol"
        ).upper()
    
    with col2:
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    if analyze_button and symbol:
        if len(symbol) < 1 or len(symbol) > 5:
            st.error("Please enter a valid stock symbol (1-5 characters)")
            return
        
        try:
            with st.spinner(f"Analyzing {symbol}... This may take a few minutes."):
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                if "Quick" in analysis_speed:
                    # Quick analysis
                    workflow = WorkflowFactory.create_investment_workflow()
                    
                    progress_bar.progress(25)
                    status_text.text("🔍 Performing quick analysis...")
                    
                    result = workflow.quick_analysis(symbol)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    
                else:
                    # Comprehensive analysis
                    workflow = WorkflowFactory.create_investment_workflow()
                    
                    # Create a placeholder for real-time updates
                    progress_placeholder = st.empty()
                    
                    with progress_placeholder.container():
                        st.info("🔍 Starting comprehensive analysis...")
                    
                    result = workflow.analyze_stock(symbol)
                    
                    progress_bar.progress(100)
                    progress_placeholder.empty()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success(f"✅ Analysis completed for {symbol}")
                
                if "Quick" in analysis_speed:
                    st.markdown(result)
                else:
                    # Display comprehensive results in tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📋 Final Report", 
                        "📊 Financial", 
                        "📈 Technical", 
                        "📰 News", 
                        "🏢 Competitive"
                    ])
                    
                    with tab1:
                        st.markdown(result["final_report"])
                    
                    with tab2:
                        st.markdown(result["financial_analysis"])
                    
                    with tab3:
                        st.markdown(result["technical_analysis"])
                    
                    with tab4:
                        st.markdown(result["news_analysis"])
                    
                    with tab5:
                        st.markdown(result["competitive_analysis"])
                
                # Download option
                st.divider()
                
                if "Quick" in analysis_speed:
                    report_content = result
                else:
                    report_content = result["final_report"]
                
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=f"{symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())


def stock_comparison_analysis():
    """Stock comparison interface"""
    
    st.header("⚖️ Stock Comparison Analysis")
    
    st.markdown("Compare multiple stocks side by side")
    
    # Input for multiple stocks
    col1, col2 = st.columns([3, 1])
    
    with col1:
        symbols_input = st.text_input(
            "Enter Stock Symbols (comma-separated):",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter 2-5 stock symbols separated by commas"
        )
    
    with col2:
        compare_button = st.button("🔄 Compare", type="primary", use_container_width=True)
    
    if compare_button and symbols_input:
        try:
            # Parse symbols
            symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]
            
            if len(symbols) < 2:
                st.error("Please enter at least 2 stock symbols")
                return
            
            if len(symbols) > 5:
                st.error("Please enter no more than 5 stock symbols")
                return
            
            with st.spinner(f"Comparing {', '.join(symbols)}... This may take several minutes."):
                
                progress_bar = st.progress(0)
                
                workflow = WorkflowFactory.create_comparison_workflow()
                result = workflow.compare_stocks(symbols)
                
                progress_bar.progress(100)
                progress_bar.empty()
            
            # Display results
            st.success(f"✅ Comparison completed for {', '.join(symbols)}")
            
            # Display in tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📋 Comparison Report",
                "📊 Financial",
                "📈 Technical", 
                "🏢 Competitive"
            ])
            
            with tab1:
                st.markdown(result["comparison_report"])
            
            with tab2:
                st.markdown(result["financial_comparison"])
            
            with tab3:
                st.markdown(result["technical_comparison"])
            
            with tab4:
                for symbol, analysis in result["competitive_analyses"].items():
                    with st.expander(f"🏢 {symbol} Competitive Analysis"):
                        st.markdown(analysis)
            
            # Download option
            st.divider()
            st.download_button(
                label="📥 Download Comparison Report",
                data=result["comparison_report"],
                file_name=f"comparison_{'_'.join(symbols)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Comparison failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())


def market_research_analysis():
    """Market research interface"""
    
    st.header("🌐 Market Research Analysis")
    
    st.markdown("Research market topics, trends, and sentiment")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "Enter Research Topic:",
            placeholder="e.g., AI stocks, renewable energy, crypto market",
            help="Enter any market-related topic or trend"
        )
    
    with col2:
        research_button = st.button("🔬 Research", type="primary", use_container_width=True)
    
    if research_button and topic:
        try:
            with st.spinner(f"Researching '{topic}'... This may take a few minutes."):
                
                progress_bar = st.progress(0)
                
                workflow = WorkflowFactory.create_research_workflow()
                result = workflow.research_market_topic(topic)
                
                progress_bar.progress(100)
                progress_bar.empty()
            
            # Display results
            st.success(f"✅ Research completed for '{topic}'")
            
            # Display in tabs
            if "financial_context" in result:
                tab1, tab2, tab3 = st.tabs(["📋 Research Report", "🌐 Web Research", "📊 Related Stocks"])
                
                with tab1:
                    st.markdown(result["research_report"])
                
                with tab2:
                    st.markdown(result["web_research"])
                
                with tab3:
                    for symbol, analysis in result["financial_context"].items():
                        with st.expander(f"📊 {symbol} Analysis"):
                            st.markdown(analysis)
            else:
                tab1, tab2 = st.tabs(["📋 Research Report", "🌐 Web Research"])
                
                with tab1:
                    st.markdown(result["research_report"])
                
                with tab2:
                    st.markdown(result["web_research"])
            
            # Download option
            st.divider()
            st.download_button(
                label="📥 Download Research Report",
                data=result["research_report"],
                file_name=f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Research failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())


def custom_query_analysis():
    """Custom query interface"""
    
    st.header("❓ Custom Query Analysis")
    
    st.markdown("Ask any investment-related question")
    
    # Examples
    with st.expander("💡 Example Queries"):
        st.markdown("""
        - "What's the outlook for AAPL based on recent earnings?"
        - "Compare NVDA vs AMD for AI investments"
        - "Should I buy Tesla stock right now?"
        - "What are the risks of investing in tech stocks?"
        - "Analyze the semiconductor sector performance"
        """)
    
    query = st.text_area(
        "Enter Your Question:",
        placeholder="Ask any investment-related question...",
        height=100,
        help="Be specific about stocks, sectors, or investment topics"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        ask_button = st.button("🤔 Analyze Query", type="primary", use_container_width=True)
    
    if ask_button and query:
        try:
            with st.spinner("Processing your query... This may take a few minutes."):
                
                progress_bar = st.progress(0)
                
                workflow = WorkflowFactory.create_custom_workflow()
                result = workflow.process_query(query)
                
                progress_bar.progress(100)
                progress_bar.empty()
            
            # Display result
            st.success("✅ Query processed successfully")
            st.markdown(result)
            
            # Download option
            st.divider()
            st.download_button(
                label="📥 Download Response",
                data=result,
                file_name=f"query_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Query processing failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())


# Footer
def show_footer():
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🤖 Powered by AGNO Framework & Gemini AI | 
        📊 Real-time market data via YFinance | 
        🌐 Web research via DuckDuckGo</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    show_footer()