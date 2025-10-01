import pytest
from fastapi.testclient import TestClient # PENTING: Import TestClient, bukan AsyncClient
from app.main import app
from app.users import crud

# Fixture untuk membersihkan DB, ini tidak berubah
@pytest.fixture(autouse=True)
def clean_db():
    crud.fake_users_db.clear()
    crud.next_user_id = 1
    yield

# Inisialisasi client di sini untuk digunakan di semua tes
client = TestClient(app)

def test_create_user():
    # Fungsi tes ini tidak lagi menggunakan async/await
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "role": "staff",
        "password": "TestPassword1!"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_read_users_as_admin():
    # Buat user dulu sebagai data awal untuk tes ini
    client.post("/users/", json={
        "username": "testuser", "email": "test@example.com", "role": "staff", "password": "TestPassword1!"
    })
    
    # Jalankan tes yang sebenarnya
    response = client.get("/users/", headers={"user-role": "admin"})
    
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_read_users_as_staff_fail():
    response = client.get("/users/", headers={"user-role": "staff"})
    assert response.status_code == 403

def test_read_own_user_as_staff():
    # Buat user staff dulu untuk tes ini
    client.post("/users/", json={
        "username": "staffuser", "email": "staff@example.com", "role": "staff", "password": "Password1!"
    })
    
    # Sekarang coba ambil data diri sendiri (ID user yang baru dibuat adalah 1)
    response = client.get("/users/1", headers={"user-id": "1", "user-role": "staff"})
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_user_as_admin():
    # Buat user dulu untuk dihapus di tes ini
    client.post("/users/", json={
        "username": "usertodelete", "email": "delete@example.com", "role": "staff", "password": "Password1!"
    })

    # Jalankan tes penghapusan (ID user yang baru dibuat adalah 1)
    response = client.delete("/users/1", headers={"user-role": "admin"})
    assert response.status_code == 204
    
    # Pastikan user sudah tidak ada
    assert crud.get_user(1) is None