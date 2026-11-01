from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas import ItemCreate, ItemResponse, ItemUpdate

app = FastAPI(
    title="SaaS de Gestão de Logística e Armazenamento - MVP",
    version="1.0.0"
)

db_estoque = {}
id_counter = 1

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/itens", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_item(item: ItemCreate):
    global id_counter
    for existing_item in db_estoque.values():
        if existing_item["sku"] == item.sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SKU '{item.sku}' já cadastrado."
            )
    
    novo_item = item.model_dump()
    novo_item["id"] = id_counter
    novo_item["data_criacao"] = datetime.utcnow()
    
    db_estoque[id_counter] = novo_item
    id_counter += 1
    return novo_item

@app.get("/api/v1/itens", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def listar_itens():
    return list(db_estoque.values())
