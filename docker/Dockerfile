FROM python:3.10-slim

# отключение кэширования pip для оптимизации размера образа
ENV PIP_NO_CACHE_DIR=1 \
  # отключение проверки версии pip
  PIP_DISABLE_PIP_VERSION_CHECK=1

# установка пакетов
RUN apt-get update && apt-get install -y \
    git \
    # очистка кэша после установки пакетов
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# добавление файлов README.md и requirements.txt в контейнер (/)
COPY ./README.md ./requirements.txt /
# добавление файла print_hello.py в контейнер (/bin)
COPY ./print_hello.py /bin

# установка зависимостей
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip -r /requirements.txt

# добавление исходного кода приложения
COPY ./app /app

# создание пользователя
RUN adduser deploy2022user
# пользователь, от имени которого будет работать приложение
USER deploy2022user

# запуск приложения FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8898"]
