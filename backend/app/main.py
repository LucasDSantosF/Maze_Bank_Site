from fastapi import FastAPI
from api import auth, user, pix, extrato, transactions, contatos
from models import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pix.router)
app.include_router(extrato.router)
app.include_router(transactions.router)
app.include_router(contatos.router)