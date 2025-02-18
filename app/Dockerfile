FROM python:3.12

RUN apt update && apt install -y \
    libpq-dev gcc build-essential curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
RUN chmod +x run.sh
