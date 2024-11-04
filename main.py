from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional
import asyncpg
import os
from datetime import datetime

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

class User(BaseModel):
    id: UUID
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    sms: Optional[str] = None
    created: datetime
    lastseen: Optional[datetime] = None

class UserCreateUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    sms: Optional[str] = None

async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

@app.get("/users", response_model=list[User])
async def get_all_users():
    conn = await connect_db()
    users = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return [dict(user) for user in users]

@app.get("/users/{userid}", response_model=User)
async def get_user(userid: UUID):
    conn = await connect_db()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", userid)
    await conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

@app.post("/users", response_model=User)
async def create_user(user_data: UserCreateUpdate):
    if not user_data.email and not user_data.sms:
        raise HTTPException(status_code=400, detail="Provide either email or sms")

    conn = await connect_db()
    new_user_id = uuid4()
    await conn.execute(
        "INSERT INTO users (id, username, name, email, sms, created) VALUES ($1, $2, $3, $4, $5, $6)",
        new_user_id, user_data.username, user_data.name, user_data.email, user_data.sms, datetime.utcnow()
    )
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", new_user_id)
    await conn.close()
    return dict(user)

@app.put("/users/{userid}", response_model=User)
async def update_user(userid: UUID, user_data: UserCreateUpdate):
    conn = await connect_db()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", userid)
    if user is None:
        await conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    await conn.execute(
        """
        UPDATE users
        SET username = COALESCE($1, username),
            name = COALESCE($2, name),
            email = COALESCE($3, email),
            sms = COALESCE($4, sms),
            lastseen = $5
        WHERE id = $6
        """,
        user_data.username, user_data.name, user_data.email, user_data.sms, datetime.utcnow(), userid
    )
    updated_user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", userid)
    await conn.close()
    return dict(updated_user)

@app.delete("/users/{userid}")
async def delete_user(userid: UUID):
    conn = await connect_db()
    result = await conn.execute("DELETE FROM users WHERE id = $1", userid)
    await conn.close()
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted successfully"}
