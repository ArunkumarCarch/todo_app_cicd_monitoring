# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Initialize and expose Prometheus metrics
instrumentator = Instrumentator().instrument(app).expose(app)

# Allow React (port 3000) to talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

class TodoIn(BaseModel):
    task: str

@app.get("/api")
def root():
    return {"message": "FastAPI running"}

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/todos")
def create_todo(todo: TodoIn):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id;", (todo.task,))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": todo_id, "task": todo.task}

@app.get("/api/todos")
def list_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task FROM todos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "task": r[1]} for r in rows]


