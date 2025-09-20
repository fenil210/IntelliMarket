#!/usr/bin/env python3

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.config import Config

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("🚀 IntelliMarket Research Platform")
    print("=" * 60)
    print(f"📊 Backend API: http://{Config.HOST}:{Config.PORT}")
    print(f"🌐 Frontend: Open frontend/index.html in your browser")
    print(f"📋 Health Check: http://{Config.HOST}:{Config.PORT}/health")
    print(f"🔧 Debug Mode: {Config.DEBUG}")
    print("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )