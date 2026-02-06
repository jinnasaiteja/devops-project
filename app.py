from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="db",
        database="devopsdb",
        user="postgres",
        password="postgres"
    )

@app.on_event("startup")
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price INT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.post("/products")
def add_product(name: str, price: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s)",
        (name, price)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Product added"}

@app.get("/products")
def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


