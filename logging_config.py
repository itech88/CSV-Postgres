import logging
from datetime import datetime
import os

# Generate a timestamped log
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#if a log folder doesn't exist, create it
# figure out how to make the logfile be for each specific microfunction
if not os.path.exists('logs'):
    os.makedirs('logs')
log_filename = f"logs/logfile_{timestamp}.log"

# Setup logging
   

def configure_logging(name):
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)
