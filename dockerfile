FROM python:3.11-slim

# ---------- ENV ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- WORKDIR ----------
WORKDIR /workspace

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---------- INSTALL POETRY ----------
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# ---------- CONFIG ----------
RUN poetry config virtualenvs.create false

# ---------- DEFAULT ----------
CMD ["bash"]
