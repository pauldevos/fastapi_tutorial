# README

### Run Server

```bash
# app.main is the folder then main.py file
# if you are inside directory app, don't need it
# uvicorn python_filename:fastapi_app --reload
uvicorn directory.main:app --reload
unicorn app.main:app --reload
```

### Check JSON, Endpoints, API Docs

- OpenAPI schema: http://127.0.0.1:8000/openapi.json
- Alt Documentation: http://127.0.0.1:8000/redoc
- Swagger Docs: http://127.0.0.1:8000/docs

### Test out endpoints

```URL

http://127.0.0.1:8000/items/2?q=this+is+my+search+query

http://127.0.0.1:8000
```

## Docker

```bash
# build docker image
docker build -t fastapi_example .

# to run the Docker container w/o docker-compose
docker run --name app -p 8000:8000 fastapi_example
```

### Postgres Docker

```bash
$ docker run \
  --rm   \
  --name  postgres \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -d postgres
```

### `main.py` file options

```python
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
class User(BaseModel):
    first_name: str
    last_name: str = None
    age: int
app = FastAPI()
@app.post("/user/", response_model=User)
async def create_user(user: User):
    return user
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Iteration #2 of `main.py`

```python

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, index=True)
    last_name = Column(String)
    age = Column(Integer,)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class UserSchema(BaseModel):
    first_name: str
    last_name: str = None
    age: int

class Config:
    orm_mode = True

@app.post("/user/", response_model=UserSchema)
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    _user = UserModel(
        first_name = user.first_name,
        last_name = user.last_name,
        age = user.age
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user

@app.get("/user/", response_model=UserSchema)
async def get_user(first_name: str, db: Session = Depends(get_db)):
    _user = db.query(UserModel).filter_by(first_name=first_name).first()
    return _user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

```bash
# run main
$ python main.py
```

#### Using Docker-compose, need bash after starting container

Perhaps we need shell access to the container, maybe we need to execute a command inside, check logs or files.

```bash
docker-compose run app bash
```

### Pydantic Models vs SQLalchemy Models

To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file `models.py` with the `SQLAlchemy models`, and the file `schemas.py` with the `Pydantic models`.
These Pydantic models define more or less a "schema" (a valid data shape).
So this will help us avoiding confusion while using both.
