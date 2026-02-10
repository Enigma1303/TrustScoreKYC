FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app

USER django

CMD ["sh", "-c", "python wait_for_db.py && python manage.py runserver 0.0.0.0:8000 --noreload"]


