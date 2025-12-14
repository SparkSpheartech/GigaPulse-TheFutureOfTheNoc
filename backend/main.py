from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import api, graph, agents
import uvicorn
from pydantic import BaseModel

# Create tables (introspection simulation)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GigaPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

# Serve Static Files
# Get absolute path to frontend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Auth Models
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login(request: LoginRequest):
    # Mock Authentication
    # Any password works for now, or specific ones could be enforced
    if request.username and request.password:
        return JSONResponse(content={"success": True, "token": "mock-jwt-token-12345"})
    else:
         raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_dir, "login.html"))

@app.get("/dashboard")
async def read_dashboard():
    return FileResponse(os.path.join(frontend_dir, "dashboard.html"))

app.include_router(api.router, prefix="/api")
app.include_router(graph.router, prefix="/api/graph")
app.include_router(agents.router, prefix="/api/agents")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    # Seed data on startup
    from seed_data import seed_data
    try:
        seed_data()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")

    # Open browser automatically
    import webbrowser
    webbrowser.open("http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
