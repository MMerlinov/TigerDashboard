from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class RegisterModel(BaseModel):
    username: str
    password: str
    role: str

def init_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS system_users (username TEXT, password TEXT, role TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.post("/api/register")
async def register(data: RegisterModel):
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO system_users VALUES (?, ?, ?)", (data.username, data.password, data.role))
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)