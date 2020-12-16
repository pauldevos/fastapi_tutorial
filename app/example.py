from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PlayerCard(BaseModel):
    player_id: str
    first_name: str
    last_name: str
    
