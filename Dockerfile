FROM ollama/ollama:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-render.txt .
RUN python3 -m venv /opt/venv \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-render.txt

COPY . .

RUN chmod +x scripts/start-render.sh

EXPOSE 10000

ENTRYPOINT []
CMD ["bash", "scripts/start-render.sh"]
