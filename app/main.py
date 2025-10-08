# app/main.py
from fastapi import FastAPI
from app.routers import admin_products  # pastikan file ini ada dan namanya tepat

# >>> WAJIB: objek bernama 'app' persis seperti ini <<<
app = FastAPI(
    title="Shopping Cart API (UTS)",
    description="Backend e-commerce in-memory (tanpa DB/JWT) — Admin Produk",
    version="0.1.0",
)

# daftar router
app.include_router(admin_products.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Shopping Cart API running"}
