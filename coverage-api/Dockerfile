FROM python:3.11.7-slim-bookworm

WORKDIR /src

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-config", "log_config.json"]


