# di tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app  # Impor instance aplikasi FastAPI

# Buat instance TestClient
client = TestClient(app)

def test_read_root():
    """Menguji endpoint root."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Selamat datang di Shopping Cart API"}

def test_get_all_products():
    """Menguji pengambilan semua produk."""
    response = client.get("/products")
    assert response.status_code == 200
    # Memastikan respons adalah sebuah list
    assert isinstance(response.json(), list)

def test_create_product_success():
    """Menguji pembuatan produk baru yang berhasil."""
    product_data = {
        "name": "SSD 1TB",
        "price": 150.00,
        "stock": 100
    }
    response = client.post("/admin/products", json=product_data)
    assert response.status_code == 201  # 201 Created
    response_data = response.json()
    assert response_data["name"] == product_data["name"]
    assert "id" in response_data

def test_create_product_invalid_price():
    """Menguji pembuatan produk dengan harga tidak valid."""
    product_data = {
        "name": "Invalid Product",
        "price": -10.0, # Harga negatif
        "stock": 10
    }
    response = client.post("/admin/products", json=product_data)
    # FastAPI/Pydantic secara otomatis mengembalikan 422 untuk data yang tidak dapat diproses
    assert response.status_code == 422

def test_checkout_empty_cart():
    """Menguji proses checkout dengan keranjang kosong."""
    # Pastikan keranjang kosong (mungkin perlu di-reset antar tes jika state persisten)
    # Untuk aplikasi ini, state di-reset setiap kali TestClient dibuat
    response = client.post("/cart/checkout", json={"promo_code": None})
    assert response.status_code == 400
    assert response.json()["detail"] == "Keranjang belanja kosong"

#... Tambahkan test case untuk setiap endpoint lainnya