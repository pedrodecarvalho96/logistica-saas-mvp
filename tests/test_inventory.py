from fastapi.testclient import TestClient
from app.main import app, db_estoque, id_counter

client = TestClient(app)

def setup_function():
    db_estoque.clear()
    global id_counter
    id_counter = 1

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_cadastrar_item_sucesso():
    payload = {
        "sku": "BOX-001",
        "nome": "Caixa Organizadora",
        "categoria": "Armazenamento",
        "quantidade": 100,
        "localizacao_galpao": "Corredor A1",
        "preco_unitario": 35.50
    }
    response = client.post("/api/v1/itens", json=payload)
    assert response.status_code == 201
    assert response.json()["sku"] == "BOX-001"

def test_impedir_sku_duplicado():
    payload = {
        "sku": "BOX-001",
        "nome": "Caixa Organizadora",
        "categoria": "Armazenamento",
        "quantidade": 100,
        "localizacao_galpao": "Corredor A1",
        "preco_unitario": 35.50
    }
    client.post("/api/v1/itens", json=payload)
    response = client.post("/api/v1/itens", json=payload)
    assert response.status_code == 400

def test_listar_itens():
    response = client.get("/api/v1/itens")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
