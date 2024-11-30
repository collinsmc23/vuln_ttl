import logging
import socket
import json

HOST, PORT = "localhost", 9999

logger = logging.getLogger("client")
logger.setLevel(logging.DEBUG)

class SocketHandler(logging.Handler):
    def __init__(self, host, port):
        super().__init__()
        self.address = (host, port)
        self.sock = socket.create_connection(self.address)

    def emit(self, record):
        try:
            # Convert the LogRecord to a dictionary and serialize to JSON
            log_entry = self.format(record)
            log_dict = record.__dict__
            log_dict['msg'] = log_entry  # Include the formatted message
            self.sock.sendall((json.dumps(log_dict) + "\n").encode("utf-8"))
        except Exception as e:
            print(f"Failed to send log: {e}")

    def close(self):
        self.sock.close()
        super().close()

# Add the custom SocketHandler to the logger
handler = SocketHandler(HOST, PORT)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Send a log message
logger.info("This is an info message from the client.")
