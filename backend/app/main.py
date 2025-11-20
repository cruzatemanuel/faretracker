from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, fare
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fair Fares API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(fare.router)

@app.get("/")
def root():
    return {"message": "Fair Fares API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

