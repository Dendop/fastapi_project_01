from fastapi import FastAPI
from . import model
from .database import engine
from .routers import post, user, authentication, vote
from fastapi.middleware.cors import CORSMiddleware

#since Iam using the alembic not really needed
model.Base.metadata.create_all(bind=engine) #initializing db when running the main

origins = ['https://www.google.com',
           "http://localhost.tiangolo.com",
            "https://localhost.tiangolo.com",
            "http://localhost",
            "http://localhost:8080",
        ]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"message": "Hello, World"}


    
