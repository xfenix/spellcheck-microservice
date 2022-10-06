ARG USERNAME=snippet-microservice-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID
ARG WORKDIR=/srv/www/

FROM python:3.10.7-slim as builder
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
RUN apt-get update -y
RUN apt-get install -y enchant-2 hunspell-ru hunspell-es hunspell-de-de hunspell-fr hunspell-pt-pt
RUN pip install --no-cache-dir install "poetry==1.2.1"
RUN poetry config virtualenvs.create false
RUN poetry install
RUN rm poetry.lock
RUN pip uninstall -y poetry
RUN mkdir /data/
RUN chmod 777 /data/

FROM python:3.10.7-slim as runtime
ARG USERNAME
ARG WORKDIR
WORKDIR $WORKDIR
COPY --from=builder / /
USER $USERNAME
ENV SPELLCHECK_ENABLE_CORS=false
CMD ["python", "-m", "whole_app"]
