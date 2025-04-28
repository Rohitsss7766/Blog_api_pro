# app/logger.py
import os
import logging

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", mode="a"),  # Append to log file
        logging.StreamHandler()  # Also print to console
    ]
)

# Shared logger instance
logger = logging.getLogger("blog-api")
