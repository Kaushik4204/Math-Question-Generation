import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Key for authentication
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# Model names for text/chat and image generation
MODEL_NAME: str = "models/gemini-1.5-flash"  # Text/chat generation model
IMAGE_MODEL: str = "models/gemini-1.5-pro"   # Image generation model

# Image size configuration (width x height)
IMAGE_SIZE: str = "512x512"

# Ensure API key is provided
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env file or environment variables.")
