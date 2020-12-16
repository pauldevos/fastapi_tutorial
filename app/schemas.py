from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None 

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int 

    class Config:
        orm_mode = True 


class UserBase(BaseModel):
    email: str 


class UserCreate(UserBase):
    password: str 


class User(UserBase):
    id: int 
    is_active: bool 
    items: List[Item] = []

    class Config:
        orm_mode = True # allows grabbing as an attribute instead of only python dict
                        # e.g. class.attr vs only class['attr']
                        # Without orm_mode, if you returned a SQLAlchemy model from your path operation, 
                        # it wouldn't include the relationship data. 
                        # Even if you declared those relationships in your Pydantic models.