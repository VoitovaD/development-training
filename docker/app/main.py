from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_root() -> None:
    """
    Путь "GET /".

    :return:
    """

    return None
