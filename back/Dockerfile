FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Playwright dependencies first
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u12 \
    build-essential=12.9 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libexpat1 \
    # Other build tools
    && pip install --no-cache-dir --upgrade --root-user-action=ignore pip==24.0 \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s ~/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get remove -y curl build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Install Playwright browsers
RUN playwright install \
    && playwright install-deps

COPY . .
    
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload"]
