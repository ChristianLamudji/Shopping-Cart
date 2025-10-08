# di app/routers/user.py
from fastapi import APIRouter
from typing import List
from.. import schemas, services

router = APIRouter(
    tags=["User"]
)

@router.get("/products", response_model=List[schemas.Product])
def get_all_products():
    return services.get_all_available_products()

@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product_details(product_id: int):
    return services.get_product_by_id(product_id)

@router.get("/cart", response_model=schemas.ShoppingCart)
def view_cart():
    return services.get_current_cart()

@router.post("/cart/items", response_model=schemas.ShoppingCart)
def add_to_cart(item_data: schemas.CartItemAdd):
    return services.add_item_to_cart(item_data)

#... (Endpoint untuk PUT dan DELETE item keranjang)

@router.post("/cart/checkout", response_model=schemas.TransactionSummary)
def checkout(checkout_data: schemas.CheckoutRequest):
    return services.process_checkout(checkout_data)