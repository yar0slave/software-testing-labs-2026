"""Локальный учебный стенд. Запуск: python server.py."""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            body = json.dumps({'status': 'ok', 'service': 'lab-api'}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()
    def log_message(self, *args):
        pass
if __name__ == '__main__':
    web = Path(__file__).parent / 'web'
    server = ThreadingHTTPServer(('127.0.0.1', 8765), partial(Handler, directory=str(web)))
    server.request_queue_size = 128
    print('http://127.0.0.1:8765', flush=True)
    server.serve_forever()
