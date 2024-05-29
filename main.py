from fastapi import FastAPI
import models
from routers import authentication_router,product_router
from databases import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication_router)
app.include_router(product_router)
