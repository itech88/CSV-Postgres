import logging
from datetime import datetime
import os

# Generate a timestamped log
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#if a log folder doesn't exist, create it
# figure out how to make the logfile be for each specific microfunction
if not os.path.exists('logs'):
    os.makedirs('logs')
    # tell the user a log file was created and where
    print(f"Log folder created: {os.path.abspath('logs')}")
    logging.info(f"Log folder created: {os.path.abspath('logs')}")
log_filename = f"logs/logfile_{timestamp}.log"

# Setup logging
   

def configure_logging(name):
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)

# after the end of the pipeline, check to see if the log file was created
def check_log_file():
    if os.path.exists(log_filename):
        print(f"Log file created: {log_filename}")
        # tell the user where the log file is located
        print(f"Log file located at: {os.path.abspath(log_filename)}")
    else:
        print(f"Log file not created: {log_filename}")
    return