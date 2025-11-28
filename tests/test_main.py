import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# Configuração do banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables after test
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    """Testa a rota raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API Dockerizada!"}

def test_create_item(test_db):
    """Testa a criação de um item"""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item",
        "price": 100
    }
    
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "id" in data

def test_read_items(test_db):
    """Testa a listagem de itens"""
    # Primeiro cria alguns itens
    item1 = {"title": "Item 1", "description": "Desc 1", "price": 100}
    item2 = {"title": "Item 2", "description": "Desc 2", "price": 200}
    
    client.post("/items/", json=item1)
    client.post("/items/", json=item2)
    
    # Testa listagem geral
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == item1["title"]
    assert data[1]["title"] == item2["title"]

def test_read_items_with_pagination(test_db):
    """Testa a paginação na listagem de itens"""
    # Cria 3 itens
    for i in range(3):
        client.post("/items/", json={"title": f"Item {i}", "price": i * 100})
    
    # Testa limit
    response = client.get("/items/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Testa skip
    response = client.get("/items/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Item 1"

def test_read_item(test_db):
    """Testa a leitura de um item específico"""
    # Cria um item
    item_data = {"title": "Test Item", "description": "Test Desc", "price": 150}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Lê o item criado
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]
    assert data["price"] == item_data["price"]

def test_read_nonexistent_item(test_db):
    """Testa a leitura de um item que não existe"""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item(test_db):
    """Testa a atualização de um item"""
    # Cria um item
    item_data = {"title": "Original", "description": "Original Desc", "price": 100}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Atualiza o item
    update_data = {"title": "Updated", "description": "Updated Desc", "price": 200}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["price"] == update_data["price"]
    assert data["id"] == item_id

def test_update_nonexistent_item(test_db):
    """Testa a atualização de um item que não existe"""
    update_data = {"title": "Updated", "description": "Updated Desc", "price": 200}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item(test_db):
    """Testa a exclusão de um item"""
    # Cria um item
    item_data = {"title": "To Delete", "description": "Delete me", "price": 100}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Deleta o item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    
    # Verifica que o item foi deletado
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

def test_delete_nonexistent_item(test_db):
    """Testa a exclusão de um item que não existe"""
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_item_validation():
    """Testa a validação dos dados do item"""
    # Testa item sem título
    invalid_item = {"description": "No title", "price": 100}
    response = client.post("/items/", json=invalid_item)
    assert response.status_code == 422  # Unprocessable Entity
    
    # Testa item sem preço
    invalid_item = {"title": "No price", "description": "No price"}
    response = client.post("/items/", json=invalid_item)
    assert response.status_code == 422