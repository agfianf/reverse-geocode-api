FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /application
# Install the application dependencies.
RUN --mount=from=ghcr.io/astral-sh/uv:0.7.3,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-cache

# Copy the application into the container.
COPY ./src/app /application/src/app
COPY ./src/migrations /application/src/migrations
COPY ./src/alembic.ini /application/src/alembic.ini


ARG USER_UID=1000
ARG USER_GID=1000

# Create nonroot user and set permissions
RUN groupadd nonroot \
    && useradd -u ${USER_UID} -g nonroot -m -s /bin/zsh nonroot
USER nonroot

ENV PATH="/application/.venv/bin:${PATH}"
ENV PYTHONPATH=/application/src

WORKDIR /application/src
CMD ["/application/.venv/bin/uvicorn", "app.main:app", "--host",  "0.0.0.0", "--port", "8080"]
