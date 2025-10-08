from fastapi import FastAPI
# Jika folder 'routers' berada di dalam package 'app' (recommended), pakai relatif import:
from .routers import admin, user
# Jika 'routers' ada di root module (tidak direkomendasikan untuk struktur package), gunakan:
# from routers import admin, user

app = FastAPI(
    title="Shopping Cart API",
    description="API untuk mengelola produk, keranjang belanja, dan checkout.",
    version="1.0.0"
)

app.include_router(admin.router)
app.include_router(user.router)

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Selamat datang di Shopping Cart API"}
