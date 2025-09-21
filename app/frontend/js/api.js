/**
 * IntelliMarket API Client
 * Handles all API communication with the backend
 */

class IntelliMarketAPI {
    constructor() {
        this.baseURL = 'http://127.0.0.1:5000/api';
        this.timeout = 300000; // 5 minutes
        this.checkConnection();
    }

    async checkConnection() {
        try {
            const response = await fetch('http://127.0.0.1:5000/health');
            const status = document.getElementById('api-status');
            
            if (response.ok) {
                status.textContent = 'Connected';
                status.className = 'status-value connected';
            } else {
                status.textContent = 'Error';
                status.className = 'status-value error';
            }
        } catch (error) {
            const status = document.getElementById('api-status');
            status.textContent = 'Disconnected';
            status.className = 'status-value error';
        }
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            timeout: this.timeout,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout - analysis is taking longer than expected');
            }
            throw error;
        }
    }

    async downloadPDF(content, title) {
        try {
            const url = `${this.baseURL}/download/pdf`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    title: title
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Failed to generate PDF: ${response.statusText}`);
            }

            // Get the PDF blob
            const blob = await response.blob();
            
            // Create download link
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            
            // Extract filename from response headers or generate one
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'IntelliMarket_Report.pdf';
            
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }
            
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
            
            return { success: true, filename: filename };
        } catch (error) {
            throw new Error(`PDF download failed: ${error.message}`);
        }
    }

    async analyzeStock(symbol, analysisType = 'quick') {
        return await this.makeRequest('/analyze/stock', {
            method: 'POST',
            body: JSON.stringify({
                symbol: symbol,
                type: analysisType
            })
        });
    }

    async compareStocks(symbols) {
        return await this.makeRequest('/analyze/comparison', {
            method: 'POST',
            body: JSON.stringify({
                symbols: symbols
            })
        });
    }

    async marketResearch(topic) {
        return await this.makeRequest('/analyze/research', {
            method: 'POST',
            body: JSON.stringify({
                topic: topic
            })
        });
    }

    async customQuery(query) {
        return await this.makeRequest('/analyze/query', {
            method: 'POST',
            body: JSON.stringify({
                query: query
            })
        });
    }

    async validateSymbol(symbol) {
        return await this.makeRequest(`/validate/symbol/${encodeURIComponent(symbol)}`);
    }

    async getSystemInfo() {
        return await this.makeRequest('/system/info');
    }

    async analyzeStockAsync(symbol, analysisType = 'comprehensive') {
        return await this.makeRequest('/analyze/async/stock', {
            method: 'POST',
            body: JSON.stringify({
                symbol: symbol,
                type: analysisType
            })
        });
    }

    async getAnalysisStatus(taskId) {
        return await this.makeRequest(`/status/${taskId}`);
    }

    isValidSymbol(symbol) {
        return /^[A-Z]{1,5}$/.test(symbol);
    }

    parseSymbolList(symbolsText) {
        return symbolsText
            .split(',')
            .map(s => s.trim().toUpperCase())
            .filter(s => s.length > 0);
    }

    validateSymbolList(symbols) {
        if (symbols.length < 2) {
            return {
                valid: false,
                error: 'At least 2 symbols required for comparison'
            };
        }

        if (symbols.length > 5) {
            return {
                valid: false,
                error: 'Maximum 5 symbols allowed for comparison'
            };
        }

        for (const symbol of symbols) {
            if (!this.isValidSymbol(symbol)) {
                return {
                    valid: false,
                    error: `Invalid symbol format: ${symbol} (1-5 letters only)`
                };
            }
        }

        return { valid: true };
    }

    formatError(error) {
        if (typeof error === 'string') {
            return error;
        }

        if (error.message) {
            return error.message;
        }

        return 'An unexpected error occurred. Please try again.';
    }
}

class ProgressTracker {
    constructor() {
        this.loadingArea = document.getElementById('loading-area');
        this.loadingTitle = document.getElementById('loading-title');
        this.loadingMessage = document.getElementById('loading-message');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.currentProgress = 0;
        this.progressInterval = null;
    }

    show(title, message) {
        this.loadingTitle.textContent = title;
        this.loadingMessage.textContent = message;
        this.loadingArea.classList.remove('hidden');
        this.currentProgress = 0;
        this.updateProgress(0);
        this.startProgressAnimation();
        
        // Hide results while loading
        const resultsArea = document.getElementById('results-area');
        resultsArea.classList.add('hidden');
    }

    startProgressAnimation() {
        this.progressInterval = setInterval(() => {
            if (this.currentProgress < 90) {
                this.currentProgress += Math.random() * 15;
                if (this.currentProgress > 90) {
                    this.currentProgress = 90;
                }
                this.updateProgress(this.currentProgress);
            }
        }, 500);
    }

    updateProgress(percent) {
        this.progressFill.style.width = `${percent}%`;
        this.progressText.textContent = `${Math.round(percent)}%`;
    }

    complete() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        
        this.updateProgress(100);
        
        setTimeout(() => {
            this.hide();
        }, 500);
    }

    hide() {
        this.loadingArea.classList.add('hidden');
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }
}