import time
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, status
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


class ChangeDogModel(Dog):
    """
    Модель для частичного обновления ресурса
    """
    name: Optional[str] = Field(None, title="Имя собаки")
    kind: Optional[DogType] = Field(None, title="Порода собаки")


class Timestamp(BaseModel):
    """
    Timestamp-модель.
    """

    id: int = Field(..., title="Идентификатор")
    timestamp: int = Field(..., title="Дата и время")


# база данных собак
DB_DOGS = {}


@app.get("/", response_model=list[Dog])
def root() -> list[Dog]:
    """
    Путь "GET /".

    Загрузка списка собак.

    :return:
    """

    return list(DB_DOGS.values())


@app.post("/post", response_model=Timestamp)
def get_post() -> Timestamp:
    """
    Путь "POST /post".

    :return:
    """

    return Timestamp(id=0, timestamp=int(time.time(),))


@app.get("/dog", response_model=list[Dog])
def get_dogs(kind: DogType = Query(..., title="Порода собаки")) -> list[Dog]:
    """
    Получение списка собак с фильтрацией по переданной породе собаки.

    :param kind: Порода собаки.
    :return:
    """

    # получение собак с фильтрацией по породе
    return [dog for dog in DB_DOGS.values() if dog.kind == kind]


@app.post("/dog", response_model=Dog)
def create_dog(dog: Dog) -> Dog:
    """
    Запись собак.

    :param dog: Объект собаки.
    :return:
    """

    pk = dog.pk
    if not pk:
        if DB_DOGS:
            pk = max(dog.pk for dog in DB_DOGS.values()) + 1
        else:
            pk = 1

    DB_DOGS[pk] = Dog(pk=pk, name=dog.name, kind=dog.kind)

    return DB_DOGS[pk]


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int) -> Optional[Dog]:
    """
    Получение собаки по идентификатору.

    :param pk: Идентификатор.
    :return:
    """

    if dog := DB_DOGS.get(pk):
        return dog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден."
    )


@app.patch("/dog/{pk}", response_model=ChangeDogModel)
def update_dog(pk: int, dog: ChangeDogModel) -> Optional[Dog]:
    """
    Обновление собаки по идентификатору.

    :param pk: Идентификатор.
    :param dog: Данные собаки для обновления.
    :return:
    """

    if pk in DB_DOGS:
        values = dog.dict(exclude={"pk"}, exclude_none=True)
        DB_DOGS[pk] = DB_DOGS[pk].copy(update=values)

        return DB_DOGS[pk]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден."
    )
