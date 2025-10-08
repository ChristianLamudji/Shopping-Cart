# app/data.py
from typing import Dict, List, Any

# "Database" dalam memori
products_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Laptop Gaming", "price": 1500.00, "stock": 50},
    2: {"id": 2, "name": "Mouse Wireless", "price": 50.00, "stock": 200},
}

promos_db: Dict[str, Dict[str, Any]] = {
    "SAVE10": {"code": "SAVE10", "product_ids": [], "discount_percent": 10.0}
}

user_cart: Dict[int, int] = {}  # Key: product_id, Value: quantity

transactions_db: List[Dict[str, Any]] = []  # list transaksi (kosong saat mulai)

# Counter untuk ID unik
next_product_id = 3
next_transaction_id = 1
