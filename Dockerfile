ARG USERNAME=snippet-microservice-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID
ARG WORKDIR=/srv/www/

FROM python:3.10.4-slim as builder
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG WORKDIR
WORKDIR $WORKDIR
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
COPY poetry.lock .
COPY pyproject.toml .
COPY . $WORKDIR
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN rm poetry.lock
RUN pip uninstall -y poetry

FROM python:3.10.4-slim as runtime
ARG USERNAME
ARG WORKDIR
WORKDIR $WORKDIR
COPY --from=builder / /
USER $USERNAME
ENV DEBUG=False
CMD ["python", "-m", "whole_app"]
