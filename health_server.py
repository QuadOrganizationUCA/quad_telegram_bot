"""
Simple HTTP health check server for Render deployment.
Runs alongside the bot to satisfy Render's port requirement.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple handler for health check endpoints."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response = """
            <!DOCTYPE html>
            <html>
            <head><title>Quad Telegram Bot</title></head>
            <body>
                <h1>🤖 Quad Telegram Bot is Running!</h1>
                <p>✅ Bot Status: <strong>Active</strong></p>
                <p>🚀 Mission: Making education accessible everywhere for everyone</p>
                <p>👥 Team: Amirbek, Manuchehr, Asiljon</p>
                <hr>
                <p><em>This is a health check endpoint for Render deployment.</em></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress request logging to keep console clean."""
        pass


def start_health_server(port=10000):
    """Start the health check server in a background thread."""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    
    def run():
        print(f"🌐 Health check server started on port {port}")
        server.serve_forever()
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return server

