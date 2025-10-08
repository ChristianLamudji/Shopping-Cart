from typing import Dict
import itertools

# Counter ID produk (auto-increment) — tetap selama server berjalan
_product_id_counter = itertools.count(1)

# Penyimpanan in-memory (sesuai batasan UTS)
PRODUCTS: Dict[int, dict] = {}  # {id: {"id": int, "name": str, "price": float, "stock": int, "category": str|None}}

def next_product_id() -> int:
    return next(_product_id_counter)

def reset_store_for_tests():
    """Hanya dipakai oleh unit test untuk mereset state in-memory."""
    global PRODUCTS, _product_id_counter
    PRODUCTS.clear()
    _product_id_counter = itertools.count(1)
