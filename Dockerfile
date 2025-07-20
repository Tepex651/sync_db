FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv --root-user-action=ignore

RUN uv sync --locked

COPY app ./app

ENV PYTHONPATH=/app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5555"]
