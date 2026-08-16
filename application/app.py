from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg2
 
DB_CONFIG = {
    "host": "postgres",
    "database": "banking",
    "user": "banking_user",
    "password": "banking_pass",
    "port": 5432
}
 
 
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
 
 
class Handler(BaseHTTPRequestHandler):
 
    def send_json(self, status_code, response):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
 
    def do_GET(self):
 
        # Application health
        if self.path == "/health":
            response = {
                "application": "banking-api",
                "status": "UP"
            }
 
            self.send_json(200, response)
 
        # Database health
        elif self.path == "/db-health":
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
 
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
 
                cursor.close()
                conn.close()
 
                response = {
                    "application": "banking-api",
                    "database": "UP",
                    "result": result[0]
                }
 
                self.send_json(200, response)
 
            except Exception as e:
                response = {
                    "application": "banking-api",
                    "database": "DOWN",
                    "error": str(e)
                }
 
                self.send_json(500, response)
 
        # Get all accounts
        elif self.path == "/accounts":
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
 
                cursor.execute("""
                    SELECT id, account_number, customer_name, balance
                    FROM accounts
                    ORDER BY id
                """)
 
                rows = cursor.fetchall()
 
                accounts = []
 
                for row in rows:
                    accounts.append({
                        "id": row[0],
                        "account_number": row[1],
                        "customer_name": row[2],
                        "balance": float(row[3])
                    })
 
                cursor.close()
                conn.close()
 
                response = {
                    "application": "banking-api",
                    "count": len(accounts),
                    "accounts": accounts
                }
 
                self.send_json(200, response)
 
            except Exception as e:
                response = {
                    "application": "banking-api",
                    "error": str(e)
                }
 
                self.send_json(500, response)
 
        else:
            self.send_json(404, {
                "error": "Endpoint not found"
            })
 
    def do_POST(self):
 
        if self.path == "/accounts":
 
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
 
                data = json.loads(body)
 
                account_number = data["account_number"]
                customer_name = data["customer_name"]
                balance = data.get("balance", 0)
 
                conn = get_db_connection()
                cursor = conn.cursor()
 
                cursor.execute("""
                    INSERT INTO accounts
                    (account_number, customer_name, balance)
                    VALUES (%s, %s, %s)
                    RETURNING id, account_number, customer_name, balance
                """, (
                    account_number,
                    customer_name,
                    balance
                ))
 
                row = cursor.fetchone()
                conn.commit()
 
                cursor.close()
                conn.close()
 
                response = {
                    "id": row[0],
                    "account_number": row[1],
                    "customer_name": row[2],
                    "balance": float(row[3])
                }
 
                self.send_json(201, response)
 
            except Exception as e:
 
                response = {
                    "error": str(e)
                }
 
                self.send_json(400, response)
 
        else:
            self.send_json(404, {
                "error": "Endpoint not found"
            })
 
server = HTTPServer(("0.0.0.0", 8080), Handler)
 
print("Banking API started on port 8080")
 
server.serve_forever()
#testing-codeql
