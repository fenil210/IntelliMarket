/**
 * API Communication Module
 * Handles all communication with the backend API
 */

class IntelliMarketAPI {
    constructor() {
        this.baseURL = 'http://127.0.0.1:5000/api';
        this.isConnected = false;
        this.initializeAPI();
    }

    async initializeAPI() {
        try {
            await this.checkHealth();
            this.isConnected = true;
            this.updateConnectionStatus('connected');
        } catch (error) {
            console.error('Failed to connect to API:', error);
            this.isConnected = false;
            this.updateConnectionStatus('error');
        }
    }

    updateConnectionStatus(status) {
        const statusElement = document.getElementById('api-status');
        if (statusElement) {
            statusElement.textContent = status === 'connected' ? 'Connected' : 
                                      status === 'error' ? 'Error' : 'Connecting...';
            statusElement.className = `status-value ${status}`;
        }
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    async checkHealth() {
        return await this.makeRequest('/system/info');
    }

    async validateSymbol(symbol) {
        try {
            return await this.makeRequest(`/validate/symbol/${symbol.toUpperCase()}`);
        } catch (error) {
            return { valid: false, reason: 'Validation failed' };
        }
    }

    async analyzeStock(symbol, analysisType = 'quick') {
        return await this.makeRequest('/analyze/stock', {
            method: 'POST',
            body: JSON.stringify({
                symbol: symbol.toUpperCase(),
                type: analysisType
            })
        });
    }

    async compareStocks(symbols) {
        const cleanSymbols = symbols.map(s => s.trim().toUpperCase()).filter(s => s);
        
        return await this.makeRequest('/analyze/comparison', {
            method: 'POST',
            body: JSON.stringify({
                symbols: cleanSymbols
            })
        });
    }

    async marketResearch(topic) {
        return await this.makeRequest('/analyze/research', {
            method: 'POST',
            body: JSON.stringify({
                topic: topic.trim()
            })
        });
    }

    async customQuery(query) {
        return await this.makeRequest('/analyze/query', {
            method: 'POST',
            body: JSON.stringify({
                query: query.trim()
            })
        });
    }

    async analyzeStockAsync(symbol, analysisType = 'comprehensive') {
        return await this.makeRequest('/analyze/async/stock', {
            method: 'POST',
            body: JSON.stringify({
                symbol: symbol.toUpperCase(),
                type: analysisType
            })
        });
    }

    async getAnalysisStatus(taskId) {
        return await this.makeRequest(`/status/${taskId}`);
    }

    // Utility methods
    formatError(error) {
        if (error.message) {
            return error.message;
        }
        return 'An unexpected error occurred. Please try again.';
    }

    isValidSymbol(symbol) {
        return /^[A-Z]{1,5}$/.test(symbol.toUpperCase());
    }

    parseSymbolList(input) {
        return input.split(',')
                   .map(s => s.trim().toUpperCase())
                   .filter(s => s && this.isValidSymbol(s));
    }

    validateSymbolList(symbols) {
        if (symbols.length < 2) {
            return { valid: false, error: 'Please enter at least 2 symbols' };
        }
        if (symbols.length > 5) {
            return { valid: false, error: 'Maximum 5 symbols allowed' };
        }
        
        const invalidSymbols = symbols.filter(s => !this.isValidSymbol(s));
        if (invalidSymbols.length > 0) {
            return { valid: false, error: `Invalid symbols: ${invalidSymbols.join(', ')}` };
        }
        
        return { valid: true };
    }
}

// Progress tracking for long-running operations
class ProgressTracker {
    constructor(containerId = 'loading-area') {
        this.container = document.getElementById(containerId);
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.loadingTitle = document.getElementById('loading-title');
        this.loadingMessage = document.getElementById('loading-message');
        
        this.currentProgress = 0;
        this.intervalId = null;
    }

    show(title = 'Processing...', message = 'This may take a few minutes') {
        if (this.loadingTitle) this.loadingTitle.textContent = title;
        if (this.loadingMessage) this.loadingMessage.textContent = message;
        
        this.container.classList.remove('hidden');
        this.setProgress(0);
        this.startSimulatedProgress();
    }

    hide() {
        this.container.classList.add('hidden');
        this.stopProgress();
    }

    setProgress(percent) {
        this.currentProgress = Math.max(0, Math.min(100, percent));
        
        if (this.progressFill) {
            this.progressFill.style.width = `${this.currentProgress}%`;
        }
        
        if (this.progressText) {
            this.progressText.textContent = `${Math.round(this.currentProgress)}%`;
        }
    }

    startSimulatedProgress() {
        this.currentProgress = 0;
        this.intervalId = setInterval(() => {
            if (this.currentProgress < 90) {
                // Slow down as it approaches 90%
                const increment = Math.max(1, (90 - this.currentProgress) * 0.1);
                this.setProgress(this.currentProgress + increment);
            }
        }, 500);
    }

    complete() {
        this.setProgress(100);
        setTimeout(() => this.hide(), 500);
    }

    stopProgress() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    updateMessage(message) {
        if (this.loadingMessage) {
            this.loadingMessage.textContent = message;
        }
    }
}

// Export for use in main.js
window.IntelliMarketAPI = IntelliMarketAPI;
window.ProgressTracker = ProgressTracker;