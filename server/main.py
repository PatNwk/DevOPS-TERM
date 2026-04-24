import os
import mysql.connector
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return mysql.connector.connect(
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        host=os.getenv("MYSQL_HOST", "localhost"),
    )

@app.get("/users")
async def get_users():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from utilisateurs")
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        return {"utilisateurs": records}
    except mysql.connector.Error as exc:
        raise HTTPException(
            status_code=503, detail="Database unavailable or misconfigured"
        ) from exc
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
