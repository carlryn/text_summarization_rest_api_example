FROM python:3.8-slim-buster

# create non privileged user
ARG APP_USER=appuser
RUN useradd --create-home ${APP_USER}

# use root for privileged operations, switch user later
USER root

RUN apt-get update && apt-get install -y \
    curl \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/* 

# upgrade pip to latest version
RUN pip install --upgrade pip


ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/poetry \
    POETRY_VERSION=1.1.7
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /home/${APP_USER}/workspace
RUN git clone https://huggingface.co/sshleifer/distilbart-cnn-6-6

# copy in the config files:
COPY pyproject.toml poetry.lock ./
# install only dependencies:
RUN poetry install --no-dev --no-root

# copy in everything else and install:
COPY . .
RUN poetry install --no-dev

EXPOSE 8080
ENTRYPOINT ["uvicorn", "app.main:app"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
