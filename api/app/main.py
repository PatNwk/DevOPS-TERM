import os
from datetime import datetime
from urllib.parse import unquote, urlparse

import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

app = FastAPI(title="Hybrid Stack API")
mongo_client = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_mysql_settings():
    parsed = urlparse(os.environ["MYSQL_URL"])
    return {
        "host": parsed.hostname or "db_mysql",
        "port": parsed.port or 3306,
        "user": unquote(parsed.username or "root"),
        "password": unquote(parsed.password or ""),
        "database": parsed.path.lstrip("/"),
    }


def get_mysql_connection():
    return mysql.connector.connect(**get_mysql_settings())


def get_mongo_database():
    global mongo_client
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(
            os.environ["MONGO_URI"], serverSelectionTimeoutMS=3000
        )
    return mongo_client.blog_db


def serialize_user(row):
    if isinstance(row.get("date_creation"), datetime):
        row["date_creation"] = row["date_creation"].isoformat()
    return row


@app.get("/")
async def read_root():
    return {"message": "Hybrid stack API is running"}


@app.on_event("shutdown")
async def close_mongo_client():
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None


@app.get("/users")
async def get_users():
    conn = None
    cursor = None

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nom, email, date_creation
            FROM utilisateurs
            ORDER BY id
            """
        )
        users = [serialize_user(row) for row in cursor.fetchall()]
        return {"users": users, "count": len(users)}
    except mysql.connector.Error as exc:
        raise HTTPException(status_code=503, detail="MySQL unavailable") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


@app.get("/posts")
async def get_posts():
    try:
        cursor = get_mongo_database().posts.find({}, {"_id": 0}).sort("titre", 1)
        posts = await cursor.to_list(length=100)
        return {"posts": posts, "count": len(posts)}
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB unavailable") from exc
