from pydantic import BaseModel, Field, validator
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nama produk")
    price: float = Field(..., ge=0, description="Harga produk >= 0")
    stock: int = Field(..., ge=0, description="Stok produk >= 0")
    category: Optional[str] = Field(default=None, description="Kategori (opsional)")

    @validator("name")
    def strip_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Nama produk tidak boleh kosong")
        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: Optional[str] = None
