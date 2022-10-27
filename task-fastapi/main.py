import time
from enum import Enum
from random import randint
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


class Timestamp(BaseModel):
    """
    Timestamp-модель.
    """

    id: int = Field(..., title="Идентификатор")
    timestamp: int = Field(..., title="Дата и время")


# база данных собак
DB_DOGS = {
    "Daisy": DogType.terrier,
    "Max": DogType.terrier,
    "Charlie": DogType.bulldog,
    "Lucy": DogType.bulldog,
    "Cooper": DogType.dalmatian,
    "Milo": DogType.dalmatian,
}


@app.get("/")
def root() -> list[Dog]:
    """
    Путь "GET /".

    Загрузка списка собак.

    :return:
    """

    return [
        (Dog(pk=index, name=db_dog_name, kind=db_dog_kind))
        for index, (db_dog_name, db_dog_kind) in enumerate(DB_DOGS.items(), start=1)
    ]


@app.post("/post", response_model=Timestamp)
def get_post() -> Timestamp:
    """
    Путь "POST /post".

    :return:
    """

    return Timestamp(id=0, timestamp=time.time(),)


@app.get("/dog")
def get_dogs(kind: DogType = Query(..., title="Порода собаки")) -> list[Dog]:
    """
    Получение списка собак с фильтрацией по переданной породе собаки.

    :param kind: Порода собаки.
    :return:
    """

    # получение собак с фильтрацией по породе
    return [
        (Dog(pk=index, name=db_dog_name, kind=db_dog_kind))
        for index, (db_dog_name, db_dog_kind) in enumerate(DB_DOGS.items(), start=1)
        if db_dog_kind == kind
    ]


@app.post("/dog", response_model=Dog)
def create_dog(dog: Dog) -> Dog:
    """
    Запись собак.

    :param dog: Объект собаки.
    :return:
    """

    return Dog(pk=dog.pk if dog.pk else randint(1, 10), name=dog.name, kind=dog.kind)


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int) -> Dog:
    """
    Получение собаки по идентификатору.

    :param pk: Идентификатор.
    :return:
    """

    return Dog(pk=pk, name="string", kind=DogType.terrier)


@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, dog: Dog) -> Dog:
    """
    Обновление собаки по идентификатору.

    :param pk: Идентификатор.
    :param dog: Данные собаки для обновления.
    :return:
    """

    return Dog(pk=pk, name=dog.name, kind=dog.kind)
