from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import ProductCreate, ProductUpdate, ProductOut
from app.store import PRODUCTS, next_product_id

router = APIRouter(prefix="/products", tags=["Admin - Products"])

@router.get("", response_model=List[ProductOut])
def list_products():
    return list(PRODUCTS.values())

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product

@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate):
    # Cek nama unik (opsional, tapi rapi)
    for p in PRODUCTS.values():
        if p["name"].lower() == payload.name.lower():
            raise HTTPException(status_code=409, detail="Nama produk sudah ada")
    pid = next_product_id()
    product = {
        "id": pid,
        "name": payload.name,
        "price": float(payload.price),
        "stock": int(payload.stock),
        "category": payload.category,
    }
    PRODUCTS[pid] = product
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    update_data = payload.dict(exclude_unset=True)
    # Validasi sederhana nama unik saat update (opsional)
    if "name" in update_data:
        for pid, p in PRODUCTS.items():
            if pid != product_id and p["name"].lower() == update_data["name"].lower():
                raise HTTPException(status_code=409, detail="Nama produk sudah ada")
    product.update(update_data)
    PRODUCTS[product_id] = product
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    del PRODUCTS[product_id]
    return None
