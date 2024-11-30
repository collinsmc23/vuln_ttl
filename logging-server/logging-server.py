import logging
import socketserver
import json

class RecordLogs(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            data = self.rfile.readline().strip()
            if not data:
                break
            try:
                # Parse the JSON data to a dictionary
                log_dict = json.loads(data.decode())
                record = logging.makeLogRecord(log_dict)
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except Exception as e:
                print(f"Failed to process log record: {e}")

if __name__ == '__main__':
    logging.basicConfig(
        filename='auth.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    HOST, PORT = 'localhost', 9999

    with socketserver.ThreadingTCPServer((HOST, PORT), RecordLogs) as server:
        print(f"Logging server listening on {HOST}:{PORT}")
        server.serve_forever()
