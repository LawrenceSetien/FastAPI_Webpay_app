from pydantic_settings import BaseSettings
from functools import lru_cache
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Transbank settings
    TRANSBANK_COMMERCE_CODE: str
    TRANSBANK_API_KEY: str
    TRANSBANK_ENVIRONMENT: str = "TEST"  # Default to test environment
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    # Log the current working directory and env file existence
    cwd = os.getcwd()
    env_path = os.path.join(cwd, ".env")
    logger.info(f"Current working directory: {cwd}")
    logger.info(f"Looking for .env file at: {env_path}")
    logger.info(f".env file exists: {os.path.exists(env_path)}")
    
    try:
        settings = Settings()
        logger.info("Loaded Transbank settings:")
        logger.info(f"- Environment: {settings.TRANSBANK_ENVIRONMENT}")
        logger.info(f"- Commerce Code: {settings.TRANSBANK_COMMERCE_CODE}")
        logger.info(f"- API Key length: {len(settings.TRANSBANK_API_KEY)}")
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}")
        raise 