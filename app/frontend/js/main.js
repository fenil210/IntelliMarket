/**
 * IntelliMarket Frontend Application
 * Main application logic and UI interactions
 */

class IntelliMarketApp {
    constructor() {
        this.api = new IntelliMarketAPI();
        this.progress = new ProgressTracker();
        this.currentAnalysisType = 'stock';
        this.recentAnalyses = this.loadRecentAnalyses();
        
        this.initializeEventListeners();
        this.renderRecentAnalyses();
        this.setupSymbolValidation();
    }

    initializeEventListeners() {
        // Analysis type buttons
        document.querySelectorAll('.analysis-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchAnalysisType(btn.dataset.type));
        });

        // Form submissions
        document.getElementById('analyze-stock-btn').addEventListener('click', () => this.handleStockAnalysis());
        document.getElementById('compare-stocks-btn').addEventListener('click', () => this.handleStockComparison());
        document.getElementById('research-btn').addEventListener('click', () => this.handleMarketResearch());
        document.getElementById('query-btn').addEventListener('click', () => this.handleCustomQuery());

        // Results actions
        document.getElementById('download-btn').addEventListener('click', () => this.downloadResults());
        document.getElementById('clear-results-btn').addEventListener('click', () => this.clearResults());

        // Example queries
        document.querySelectorAll('.example-query').forEach(query => {
            query.addEventListener('click', () => {
                document.getElementById('custom-query').value = query.textContent.replace(/['"]/g, '');
            });
        });

        // Enter key handlers
        document.getElementById('stock-symbol').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleStockAnalysis();
        });

        document.getElementById('comparison-symbols').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleStockComparison();
        });

        document.getElementById('research-topic').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleMarketResearch();
        });
    }

    switchAnalysisType(type) {
        this.currentAnalysisType = type;
        
        // Update active button
        document.querySelectorAll('.analysis-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.type === type);
        });

        // Show corresponding form
        document.querySelectorAll('.analysis-form').forEach(form => {
            form.classList.toggle('active', form.id === `${type}-form`);
        });

        // Clear results
        this.clearResults();
    }

    setupSymbolValidation() {
        const symbolInput = document.getElementById('stock-symbol');
        const validationDiv = document.getElementById('symbol-validation');
        let validationTimeout;

        symbolInput.addEventListener('input', (e) => {
            const symbol = e.target.value.trim().toUpperCase();
            
            // Clear previous timeout
            if (validationTimeout) {
                clearTimeout(validationTimeout);
            }

            // Clear validation if empty
            if (!symbol) {
                validationDiv.textContent = '';
                validationDiv.className = 'symbol-validation';
                return;
            }

            // Basic format validation
            if (!this.api.isValidSymbol(symbol)) {
                validationDiv.textContent = 'Invalid format (1-5 letters only)';
                validationDiv.className = 'symbol-validation invalid';
                return;
            }

            // Debounced API validation
            validationTimeout = setTimeout(async () => {
                try {
                    validationDiv.textContent = 'Validating...';
                    validationDiv.className = 'symbol-validation';
                    
                    const result = await this.api.validateSymbol(symbol);
                    
                    if (result.valid) {
                        validationDiv.textContent = `✓ ${result.name || symbol}`;
                        validationDiv.className = 'symbol-validation valid';
                    } else {
                        validationDiv.textContent = `✗ ${result.reason || 'Symbol not found'}`;
                        validationDiv.className = 'symbol-validation invalid';
                    }
                } catch (error) {
                    validationDiv.textContent = '⚠ Unable to validate';
                    validationDiv.className = 'symbol-validation invalid';
                }
            }, 500);
        });
    }

    async handleStockAnalysis() {
        const symbolInput = document.getElementById('stock-symbol');
        const symbol = symbolInput.value.trim().toUpperCase();

        if (!symbol) {
            this.showError('Please enter a stock symbol');
            return;
        }

        if (!this.api.isValidSymbol(symbol)) {
            this.showError('Please enter a valid stock symbol (1-5 letters)');
            return;
        }

        const analysisType = document.querySelector('input[name="analysis-depth"]:checked').value;
        
        try {
            this.progress.show(
                `Analyzing ${symbol}`,
                analysisType === 'quick' ? 'Quick analysis in progress...' : 'Comprehensive analysis in progress...'
            );

            const result = await this.api.analyzeStock(symbol, analysisType);
            
            this.progress.complete();
            this.showResults(result, `${symbol} Analysis`);
            this.addToRecentAnalyses(symbol, 'stock', analysisType);
            
        } catch (error) {
            this.progress.hide();
            this.showError(this.api.formatError(error));
        }
    }

    async handleStockComparison() {
        const symbolsInput = document.getElementById('comparison-symbols');
        const symbolsText = symbolsInput.value.trim();

        if (!symbolsText) {
            this.showError('Please enter stock symbols to compare');
            return;
        }

        const symbols = this.api.parseSymbolList(symbolsText);
        const validation = this.api.validateSymbolList(symbols);

        if (!validation.valid) {
            this.showError(validation.error);
            return;
        }

        try {
            this.progress.show(
                `Comparing ${symbols.join(', ')}`,
                'Multi-stock comparison in progress...'
            );

            const result = await this.api.compareStocks(symbols);
            
            this.progress.complete();
            this.showResults(result, `${symbols.join(' vs ')} Comparison`);
            this.addToRecentAnalyses(symbols.join(', '), 'comparison');
            
        } catch (error) {
            this.progress.hide();
            this.showError(this.api.formatError(error));
        }
    }

    async handleMarketResearch() {
        const topicInput = document.getElementById('research-topic');
        const topic = topicInput.value.trim();

        if (!topic) {
            this.showError('Please enter a research topic');
            return;
        }

        try {
            this.progress.show(
                'Market Research',
                `Researching "${topic}"...`
            );

            const result = await this.api.marketResearch(topic);
            
            this.progress.complete();
            this.showResults(result, `Market Research: ${topic}`);
            this.addToRecentAnalyses(topic, 'research');
            
        } catch (error) {
            this.progress.hide();
            this.showError(this.api.formatError(error));
        }
    }

    async handleCustomQuery() {
        const queryInput = document.getElementById('custom-query');
        const query = queryInput.value.trim();

        if (!query) {
            this.showError('Please enter your question');
            return;
        }

        try {
            this.progress.show(
                'Processing Query',
                'Analyzing your question...'
            );

            const result = await this.api.customQuery(query);
            
            this.progress.complete();
            this.showResults(result, 'Custom Query Results');
            this.addToRecentAnalyses(query.substring(0, 50) + '...', 'query');
            
        } catch (error) {
            this.progress.hide();
            this.showError(this.api.formatError(error));
        }
    }

    showResults(data, title) {
        const resultsArea = document.getElementById('results-area');
        const resultsTitle = document.getElementById('results-title');
        const resultsContent = document.getElementById('results-content');

        resultsTitle.textContent = title;
        
        // Store current results for download
        this.currentResults = { data, title };

        if (data.analysis_type === 'comparison') {
            this.renderComparisonResults(data, resultsContent);
        } else if (data.analysis_type === 'comprehensive') {
            this.renderComprehensiveResults(data, resultsContent);
        } else {
            this.renderSimpleResults(data, resultsContent);
        }

        resultsArea.classList.remove('hidden');
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    }

    renderSimpleResults(data, container) {
        const content = data.result || data.research_report || data.comparison_report || 'No results available';
        
        container.innerHTML = `
            <div class="simple-results">
                ${this.formatMarkdown(content)}
            </div>
        `;
    }

    renderComprehensiveResults(data, container) {
        const result = data.result;
        
        container.innerHTML = `
            <div class="results-tabs">
                <button class="results-tab active" data-tab="final">Final Report</button>
                <button class="results-tab" data-tab="financial">Financial</button>
                <button class="results-tab" data-tab="technical">Technical</button>
                <button class="results-tab" data-tab="news">News</button>
                <button class="results-tab" data-tab="competitive">Competitive</button>
            </div>
            
            <div class="tab-content active" id="final-tab">
                ${this.formatMarkdown(result.final_report)}
            </div>
            
            <div class="tab-content" id="financial-tab">
                ${this.formatMarkdown(result.financial_analysis)}
            </div>
            
            <div class="tab-content" id="technical-tab">
                ${this.formatMarkdown(result.technical_analysis)}
            </div>
            
            <div class="tab-content" id="news-tab">
                ${this.formatMarkdown(result.news_analysis)}
            </div>
            
            <div class="tab-content" id="competitive-tab">
                ${this.formatMarkdown(result.competitive_analysis)}
            </div>
        `;

        // Add tab switching functionality
        container.querySelectorAll('.results-tab').forEach(tab => {
            tab.addEventListener('click', () => this.switchResultsTab(tab.dataset.tab));
        });
    }

    renderComparisonResults(data, container) {
        const result = data.result;
        
        container.innerHTML = `
            <div class="results-tabs">
                <button class="results-tab active" data-tab="report">Comparison Report</button>
                <button class="results-tab" data-tab="financial">Financial</button>
                <button class="results-tab" data-tab="technical">Technical</button>
                <button class="results-tab" data-tab="competitive">Competitive</button>
            </div>
            
            <div class="tab-content active" id="report-tab">
                ${this.formatMarkdown(result.comparison_report)}
            </div>
            
            <div class="tab-content" id="financial-tab">
                ${this.formatMarkdown(result.financial_comparison)}
            </div>
            
            <div class="tab-content" id="technical-tab">
                ${this.formatMarkdown(result.technical_comparison)}
            </div>
            
            <div class="tab-content" id="competitive-tab">
                ${this.renderCompetitiveAnalyses(result.competitive_analyses)}
            </div>
        `;

        // Add tab switching functionality
        container.querySelectorAll('.results-tab').forEach(tab => {
            tab.addEventListener('click', () => this.switchResultsTab(tab.dataset.tab));
        });
    }

    renderCompetitiveAnalyses(analyses) {
        let html = '';
        for (const [symbol, analysis] of Object.entries(analyses)) {
            html += `
                <div class="competitive-section">
                    <h4>${symbol} Competitive Analysis</h4>
                    ${this.formatMarkdown(analysis)}
                </div>
            `;
        }
        return html;
    }

    switchResultsTab(tabName) {
        // Update active tab
        document.querySelectorAll('.results-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Show corresponding content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });
    }

    formatMarkdown(text) {
        if (!text) return '<p>No content available</p>';
        
        // First, handle tables
        text = this.parseMarkdownTables(text);
        
        // Then handle other markdown elements
        return text
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/^(.*)$/gm, '<p>$1</p>')
            .replace(/<p><\/p>/g, '')
            .replace(/<p>(<h[1-6]>)/g, '$1')
            .replace(/(<\/h[1-6]>)<\/p>/g, '$1')
            .replace(/<p>(<ul>)/g, '$1')
            .replace(/(<\/ul>)<\/p>/g, '$1')
            .replace(/<p>(<table)/g, '$1')
            .replace(/(<\/table>)<\/p>/g, '$1');
    }

    parseMarkdownTables(text) {
        const lines = text.split('\n');
        const result = [];
        let i = 0;
        
        while (i < lines.length) {
            const line = lines[i];
            
            // Check if this line looks like a table row (contains |)
            if (line.includes('|') && line.trim().startsWith('|') && line.trim().endsWith('|')) {
                // Look ahead to see if next line is a separator (contains dashes)
                const nextLine = lines[i + 1];
                const isTableStart = nextLine && nextLine.includes('-') && nextLine.includes('|');
                
                if (isTableStart) {
                    // Parse the table
                    const tableHtml = this.parseTable(lines, i);
                    result.push(tableHtml.html);
                    i = tableHtml.nextIndex;
                    continue;
                }
            }
            
            result.push(line);
            i++;
        }
        
        return result.join('\n');
    }

    parseTable(lines, startIndex) {
        const headerLine = lines[startIndex];
        const separatorLine = lines[startIndex + 1];
        
        // Parse header
        const headers = headerLine.split('|')
            .map(cell => cell.trim())
            .filter(cell => cell !== '');
        
        // Parse data rows
        const dataRows = [];
        let currentIndex = startIndex + 2;
        
        while (currentIndex < lines.length) {
            const line = lines[currentIndex];
            
            // Stop if line doesn't look like a table row
            if (!line.includes('|') || !line.trim().startsWith('|') || !line.trim().endsWith('|')) {
                break;
            }
            
            const cells = line.split('|')
                .map(cell => cell.trim())
                .filter(cell => cell !== '');
            
            if (cells.length > 0) {
                dataRows.push(cells);
            }
            
            currentIndex++;
        }
        
        // Generate HTML table
        let tableHtml = '<table class="markdown-table">\n';
        
        // Table header
        if (headers.length > 0) {
            tableHtml += '  <thead>\n    <tr>\n';
            headers.forEach(header => {
                tableHtml += `      <th>${this.escapeHtml(header)}</th>\n`;
            });
            tableHtml += '    </tr>\n  </thead>\n';
        }
        
        // Table body
        if (dataRows.length > 0) {
            tableHtml += '  <tbody>\n';
            dataRows.forEach(row => {
                tableHtml += '    <tr>\n';
                row.forEach((cell, index) => {
                    // Ensure we don't exceed header count
                    if (index < headers.length) {
                        tableHtml += `      <td>${this.escapeHtml(cell)}</td>\n`;
                    }
                });
                tableHtml += '    </tr>\n';
            });
            tableHtml += '  </tbody>\n';
        }
        
        tableHtml += '</table>';
        
        return {
            html: tableHtml,
            nextIndex: currentIndex
        };
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showError(message) {
        // Create or update error display
        let errorDiv = document.getElementById('error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'error-message';
            errorDiv.className = 'error-message';
            document.querySelector('.content-area').insertBefore(errorDiv, document.querySelector('.analysis-form.active'));
        }

        errorDiv.innerHTML = `
            <div class="error-content">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${message}</span>
                <button class="error-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    clearResults() {
        const resultsArea = document.getElementById('results-area');
        resultsArea.classList.add('hidden');
        this.currentResults = null;
    }

    downloadResults() {
        if (!this.currentResults) return;

        const { data, title } = this.currentResults;
        let content = '';

        if (data.analysis_type === 'comprehensive') {
            content = data.result.final_report;
        } else {
            content = data.result || data.research_report || data.comparison_report;
        }

        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${title.replace(/[^a-zA-Z0-9]/g, '_')}_${new Date().toISOString().slice(0, 10)}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    addToRecentAnalyses(query, type, analysisType = null) {
        const analysis = {
            query,
            type,
            analysisType,
            timestamp: new Date().toISOString()
        };

        this.recentAnalyses.unshift(analysis);
        this.recentAnalyses = this.recentAnalyses.slice(0, 10); // Keep only 10 recent

        this.saveRecentAnalyses();
        this.renderRecentAnalyses();
    }

    renderRecentAnalyses() {
        const container = document.getElementById('recent-list');
        
        if (this.recentAnalyses.length === 0) {
            container.innerHTML = '<p class="no-recent">No recent analyses</p>';
            return;
        }

        container.innerHTML = this.recentAnalyses.map(analysis => `
            <div class="recent-item" onclick="app.loadRecentAnalysis('${analysis.query}', '${analysis.type}')">
                <div class="recent-symbol">${analysis.query}</div>
                <div class="recent-time">${this.formatTime(analysis.timestamp)}</div>
            </div>
        `).join('');
    }

    loadRecentAnalysis(query, type) {
        this.switchAnalysisType(type);
        
        if (type === 'stock') {
            document.getElementById('stock-symbol').value = query;
        } else if (type === 'comparison') {
            document.getElementById('comparison-symbols').value = query;
        } else if (type === 'research') {
            document.getElementById('research-topic').value = query;
        } else if (type === 'query') {
            document.getElementById('custom-query').value = query;
        }
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString();
    }

    saveRecentAnalyses() {
        try {
            localStorage.setItem('intelligmarket_recent', JSON.stringify(this.recentAnalyses));
        } catch (error) {
            console.warn('Failed to save recent analyses:', error);
        }
    }

    loadRecentAnalyses() {
        try {
            const saved = localStorage.getItem('intelligmarket_recent');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.warn('Failed to load recent analyses:', error);
            return [];
        }
    }
}

// Add error message styles
const errorStyles = `
    .error-message {
        background: #fed7d7;
        border: 1px solid #fc8181;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        animation: slideDown 0.3s ease;
    }
    
    .error-content {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        color: #c53030;
    }
    
    .error-close {
        margin-left: auto;
        background: none;
        border: none;
        color: #c53030;
        cursor: pointer;
        padding: 0.2rem;
        border-radius: 4px;
    }
    
    .error-close:hover {
        background: rgba(197, 48, 48, 0.1);
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .competitive-section {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .competitive-section:last-child {
        border-bottom: none;
    }
    
    .competitive-section h4 {
        color: #2d3748;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
`;

// Inject error styles
const styleSheet = document.createElement('style');
styleSheet.textContent = errorStyles;
document.head.appendChild(styleSheet);

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new IntelliMarketApp();
});