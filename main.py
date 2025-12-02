import pyodbc

# Connection string for Dockerized SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"  # You can change this to FinanceTracker if created
    "UID=sa;"
    "PWD=hani;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("✅ Connected to SQL Server!")
    print("Server version:", row[0])
except Exception as e:
    print("❌ Connection failed:", e)