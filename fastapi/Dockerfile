FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "uvicorn --host 0.0.0.0 --port $PORT --reload main:app"