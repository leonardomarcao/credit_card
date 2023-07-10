# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}

FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS builder

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements requirements
RUN pip install --no-cache-dir -r requirements/dev.txt
COPY . .
EXPOSE 5000
