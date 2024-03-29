ARG USERNAME=snippet-microservice-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID
ARG WORKDIR=/srv/www/

FROM pypy:3.10-slim as builder
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG WORKDIR
WORKDIR $WORKDIR
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
COPY poetry.lock .
COPY pyproject.toml .
RUN apt-get update -y
# install rust
RUN apt-get install -y curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# install prerequisites
RUN apt-get install -y build-essential libssl-dev enchant-2 hunspell-ru hunspell-es hunspell-de-de hunspell-fr hunspell-pt-pt
RUN pip install -U pip poetry
RUN poetry config virtualenvs.create false
# install necessary packages
RUN poetry install --compile
# massive cleanup
RUN rm poetry.lock
RUN poetry cache clear pypi --all
RUN pip uninstall -y poetry pip setuptools
RUN rustup self uninstall -y
RUN apt-get remove -y build-essential libssl-dev gcc curl
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN rm -rf /var/lib/apt/lists/*
# make necessary dirs
RUN mkdir /data/
RUN chmod 777 /data/

FROM pypy:3.10-slim as runtime
ARG USERNAME
ARG WORKDIR
WORKDIR $WORKDIR
COPY --from=builder / /
COPY . $WORKDIR
USER $USERNAME
ENV SPELLCHECK_ENABLE_CORS=false
CMD ["python", "-m", "whole_app"]
