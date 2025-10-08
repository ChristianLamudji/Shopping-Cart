# di app/routers/admin.py
from fastapi import APIRouter, status
from typing import List
from.. import schemas, services

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def add_product(product_data: schemas.ProductCreate):
    return services.create_new_product(product_data)

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product_data: schemas.ProductUpdate):
    return services.update_existing_product(product_id, product_data)

#... (Endpoint untuk DELETE /products/{product_id} dan POST /promos)