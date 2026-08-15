from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, products, sales_boost


app = FastAPI(
    title="Trend Products Analytics",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales_boost.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
