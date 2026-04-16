from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI(title="Items API")

# In-memory storage
items_db: dict[str, dict] = {}

# --- Pydantic Models ---

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float

# --- Endpoints ---

@app.get("/items", response_model=list[ItemResponse])
def list_items():
    return [ItemResponse(id=k, **v) for k, v in items_db.items()]

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    item_id = str(uuid.uuid4())[:8]
    items_db[item_id] = item.model_dump()
    return ItemResponse(id=item_id, **items_db[item_id])

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(id=item_id, **items_db[item_id])

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: str, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.model_dump(exclude_unset=True)
    items_db[item_id].update(update_data)
    return ItemResponse(id=item_id, **items_db[item_id])

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}
