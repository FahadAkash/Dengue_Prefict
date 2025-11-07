from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import json
import urllib.parse
import urllib.request
import urllib.error

class DengueRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Determine the file to serve
        if self.path == '/':
            filepath = 'index.html'
        elif self.path == '/style.css':
            filepath = 'style.css'
        elif self.path == '/script.js':
            filepath = 'script.js'
        else:
            filepath = self.path.lstrip('/')
        
        # Check if file exists
        if os.path.exists(filepath) and os.path.isfile(filepath):
            # Determine content type
            if filepath.endswith('.html'):
                content_type = 'text/html'
            elif filepath.endswith('.css'):
                content_type = 'text/css'
            elif filepath.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'text/plain'
            
            # Read and serve the file
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
        else:
            # Serve index.html for any other path (SPA routing)
            if os.path.exists('index.html'):
                with open('index.html', 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "File not found")
    
    def do_POST(self):
        if self.path == '/predict':
            # Handle prediction request by forwarding to backend API on port 8001
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward request to backend API
                backend_url = 'http://localhost:8001/predict'
                req = urllib.request.Request(
                    backend_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    backend_response = response.read()
                    status_code = response.getcode()
                
                # Send response back to frontend
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(backend_response)
                
            except urllib.error.URLError as e:
                # Backend not available, return error
                self.send_response(503)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    'error': 'Backend service unavailable',
                    'message': 'The prediction service is not running. Please start the backend API server on port 8001.'
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
            except Exception as e:
                # Other error
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
        elif self.path == '/chat':
            # Handle chat request by forwarding to backend API on port 8001
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward request to backend API chat endpoint
                backend_url = 'http://localhost:8001/chat'
                req = urllib.request.Request(
                    backend_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    backend_response = response.read()
                    status_code = response.getcode()
                
                # Send response back to frontend
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(backend_response)
                
            except urllib.error.URLError as e:
                # Backend not available, return error
                self.send_response(503)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    'error': 'Backend service unavailable',
                    'message': 'The chat service is not running. Please start the backend API server on port 8001.'
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
            except Exception as e:
                # Other error
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            # For other POST requests, send 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Override to suppress log messages
        return

def run_server():
    # Change to the frontend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, DengueRequestHandler)
    print("Dengue Risk Predictor Frontend Server")
    print("Serving at http://localhost:8000")
    print("Forwarding API requests to backend at http://localhost:8001")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()