import os
import socket

from fastapi import FastAPI

app = FastAPI(title="homelab-app")

APP_VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def root():
    return {
        "message": "Merhaba homelab!",
        "version": APP_VERSION,
        "pod": socket.gethostname(),
    }


@app.get("/health")
def health():
    return {"status": "ok"}