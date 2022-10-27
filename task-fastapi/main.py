from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class DogType(str, Enum):
    """
    Породы собак.
    """

    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    """
    Модель собаки.
    """

    pk: Optional[int] = Field(None, title="Идентификатор")
    name: str = Field(..., title="Имя собаки")
    kind: DogType = Field(..., title="Порода собаки")


@app.get("/")
def root() -> str:
    return "string"


@app.post("/post")
def get_post() -> str:
    return "string"


@app.get("/dog")
def get_dogs(kind: DogType = Query(..., title="Порода собаки")) -> str:
    return "string"


@app.post("/dog")
def create_dog(dog: Dog) -> str:
    return "string"


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int) -> Dog:
    return Dog(pk=pk, name="string", kind="terrier")


@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, dog: Dog) -> Dog:
    return Dog(pk=pk, name=dog.name, kind=dog.kind)
