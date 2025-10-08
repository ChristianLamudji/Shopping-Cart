# di app/services.py
from fastapi import HTTPException, status
from. import data, schemas
from typing import List

# --- Logika Bisnis untuk Admin ---
def create_new_product(product_data: schemas.ProductCreate) -> schemas.Product:
    new_id = data.next_product_id
    new_product = schemas.Product(id=new_id, **product_data.model_dump())
    data.products_db[new_id] = new_product.model_dump()
    data.next_product_id += 1
    return new_product

def update_existing_product(product_id: int, product_data: schemas.ProductUpdate) -> schemas.Product:
    if product_id not in data.products_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    
    stored_product_data = data.products_db[product_id]
    update_data = product_data.model_dump(exclude_unset=True)
    updated_product_data = stored_product_data.copy()
    updated_product_data.update(update_data)
    
    data.products_db[product_id] = updated_product_data
    return schemas.Product(**updated_product_data)

#... (Fungsi untuk delete_product dan create_promo)

# --- Logika Bisnis untuk User ---
def add_item_to_cart(item_data: schemas.CartItemAdd) -> schemas.ShoppingCart:
    product_id = item_data.product_id
    quantity = item_data.quantity

    if product_id not in data.products_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    
    if data.products_db[product_id]["stock"] < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stok tidak mencukupi")

    current_quantity = data.user_cart.get(product_id, 0)
    data.user_cart[product_id] = current_quantity + quantity
    
    return get_current_cart()

#... (Fungsi untuk update_cart_item, remove_cart_item, get_current_cart)

def process_checkout(checkout_data: schemas.CheckoutRequest) -> schemas.TransactionSummary:
    if not data.user_cart:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Keranjang belanja kosong")

    cart = get_current_cart()
    subtotal = cart.subtotal
    discount = 0.0
    promo_code = checkout_data.promo_code

    if promo_code:
        if promo_code not in data.promos_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kode promo tidak valid")
        
        promo = data.promos_db[promo_code]
        discountable_amount = 0
        for item in cart.items:
            if item.product.id in promo["product_ids"]:
                discountable_amount += item.product.price * item.quantity
        
        discount = (discountable_amount * promo["discount_percent"]) / 100

    total = subtotal - discount

    # Kurangi stok produk
    for product_id, quantity in data.user_cart.items():
        data.products_db[product_id]["stock"] -= quantity

    # Buat catatan transaksi
    transaction_id = data.next_transaction_id
    transaction = {
        "transaction_id": transaction_id,
        "items": [item.model_dump() for item in cart.items],
        "subtotal": subtotal,
        "discount_applied": discount,
        "total": total,
        "message": "Checkout berhasil"
    }
    data.transactions_db.append(transaction)
    data.next_transaction_id += 1
    
    # Kosongkan keranjang
    data.user_cart.clear()
    
    return schemas.TransactionSummary(**transaction)

    # Tambahkan ini di dalam app/services.py

def get_all_available_products() -> List[schemas.Product]:
    """Mengambil semua produk dari database dalam memori."""
    return list(data.products_db.values())

def get_product_by_id(product_id: int) -> schemas.Product:
    """Mengambil satu produk berdasarkan ID."""
    if product_id not in data.products_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    return data.products_db[product_id]