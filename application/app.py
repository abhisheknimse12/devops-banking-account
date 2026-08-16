from http.server import BaseHTTPRequestHandler, HTTPServer
import json
 
 
class Handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
 
        if self.path == "/health":
            response = {
                "application": "banking-api",
                "status": "UP"
            }
 
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
 
            self.wfile.write(json.dumps(response).encode())
 
        else:
            self.send_response(404)
            self.end_headers()
 
 
server = HTTPServer(("0.0.0.0", 8080), Handler)
 
print("Banking API started on port 8080")
 
server.serve_forever()
