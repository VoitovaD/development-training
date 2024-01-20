FROM python:3.10-slim

COPY ./requirements.txt /

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ADD ./src /src
WORKDIR /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
