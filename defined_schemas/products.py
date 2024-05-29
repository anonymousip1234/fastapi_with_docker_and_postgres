from pydantic import BaseModel
from typing import Optional

class CreateProduct(BaseModel):
    name : str
    category : str
    price : float
    class config:
        orm_mode = True
class UpdateProduct(BaseModel):
    name : Optional[str] = None
    category : Optional[str] = None
    price : Optional[float] = None
    class config:
        orm_mode = True
