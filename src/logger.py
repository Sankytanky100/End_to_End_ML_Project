import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Define log file name based on current datetime
log_file = datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + ".log"

# Set up logging configuration
logging.basicConfig(
    filename=os.path.join(logs_dir, log_file), 
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info('Logging has started')
