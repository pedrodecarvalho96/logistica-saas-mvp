from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=20, description="Código SKU do produto")
    nome: str = Field(..., min_length=2, max_length=100)
    categoria: str
    quantidade: int = Field(..., ge=0)
    localizacao_galpao: str
    preco_unitario: float = Field(..., gt=0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade: Optional[int] = Field(None, ge=0)
    localizacao_galpao: Optional[str] = None
    preco_unitario: Optional[float] = Field(None, gt=0)

class ItemResponse(ItemBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
