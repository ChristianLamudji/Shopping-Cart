# di app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Model Dasar ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nama produk")
    price: float = Field(..., gt=0, description="Harga produk harus lebih besar dari 0")
    stock: int = Field(..., ge=0, description="Stok produk tidak boleh negatif")

class PromoBase(BaseModel):
    code: str = Field(..., min_length=1, description="Kode promo unik")
    discount_percent: float = Field(..., gt=0, le=100, description="Persentase diskon (1-100)")
    product_ids: List[int] = Field(..., description="Daftar ID produk yang berlaku untuk promo")

# --- Skema untuk Endpoint ---
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class Product(ProductBase):
    id: int

class PromoCreate(PromoBase):
    pass

class Promo(PromoBase):
    pass

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Jumlah harus lebih besar dari 0")

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Jumlah harus lebih besar dari 0")

class CartItem(BaseModel):
    product: Product
    quantity: int

class ShoppingCart(BaseModel):
    items: List[CartItem]
    subtotal: float

class CheckoutRequest(BaseModel):
    promo_code: Optional[str] = None

class TransactionSummary(BaseModel):
    transaction_id: int
    items: List[CartItem]
    subtotal: float
    discount_applied: float
    total: float
    message: str