FROM python:3.11-rc-bullseye as builder

ARG WORKDIR=/srv/www/
ARG USERNAME=snippet-microservice-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID

WORKDIR $WORKDIR

RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install poetry
RUN poetry install
RUN rm poetry.lock
RUN pip uninstall -y poetry


FROM python:3.11-rc-bullseye as runtime
COPY --from=builder / /
USER $USERNAME
ENV DEBUG=False
CMD ["python", "-m", "whole-app"]
