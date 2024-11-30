import re
import time
import logging
import socket
import subprocess

# Remote logging server configuration
LOGGING_SERVER_IP = "your.logging.server.ip"  # Replace with the public IP of the logging server
LOGGING_SERVER_PORT = 9999

# Configure local logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Configure socket connection for sending logs
def send_to_logging_server(message):
    try:
        with socket.create_connection((LOGGING_SERVER_IP, LOGGING_SERVER_PORT)) as sock:
            sock.sendall(message.encode() + b'\n')
    except Exception as e:
        logging.error(f"Failed to send log to logging server: {e}")

# Function to parse and monitor auth.log
def monitor_auth_log(log_path):
    login_success_pattern = re.compile(r"Accepted .* for .* from .*")
    login_failure_pattern = re.compile(r"Failed password for .* from .*")

    with open(log_path, 'r') as logfile:
        logfile.seek(0, 2)  # Move to the end of the file
        logging.info(f"Monitoring {log_path} for login attempts...")

        while True:
            line = logfile.readline()
            if not line:
                time.sleep(1)  # Sleep briefly before checking for new lines
                continue

            line = line.strip()
            if login_success_pattern.search(line):
                logging.info(f"Successful login detected: {line}")
                send_to_logging_server(line)
                initiate_shutdown()
            elif login_failure_pattern.search(line):
                logging.warning(f"Failed login attempt: {line}")
                send_to_logging_server(line)

# Function to initiate shutdown
def initiate_shutdown():
    logging.critical("Initiating shutdown due to a successful login attempt!")
    try:
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to shut down the instance: {e}")

if __name__ == "__main__":
    try:
        monitor_auth_log("/var/log/auth.log")
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
