import uvicorn
from fastapi import FastAPI
from src.database.db import Base, engine
from src.api.contacts import router as contacts_router
import src.database.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API", version="1.0.0")
app.include_router(contacts_router)


@app.get("/", tags=["Health"])
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
