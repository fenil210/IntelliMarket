import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Agent Configuration
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # Streamlit Configuration
    PAGE_TITLE = "IntelliMarket Research Platform"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    
    # Validation
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        return True