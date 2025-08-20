ARG USERNAME=snippet-microservice-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID
ARG WORKDIR=/srv/www/

FROM pypy:3.11-slim AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG WORKDIR
WORKDIR $WORKDIR
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
RUN apt-get update -y
# install rust
RUN apt-get install -y curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# install prerequisites
RUN apt-get install -y build-essential libssl-dev enchant-2 hunspell-ru hunspell-es hunspell-de-de hunspell-fr hunspell-pt-pt
RUN pip install -U pip uv
# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
# massive cleanup
RUN uv cache clean
RUN pip uninstall -y pip setuptools
RUN rustup self uninstall -y
RUN apt-get remove -y build-essential libssl-dev gcc curl
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN rm -rf /var/lib/apt/lists/*
# make necessary dirs
RUN mkdir /data/
RUN chmod 777 /data/

FROM pypy:3.11-slim AS runtime
ARG USERNAME
ARG WORKDIR
WORKDIR $WORKDIR
COPY --from=builder / /
COPY . $WORKDIR
USER $USERNAME
ENV PATH="$WORKDIR/.venv/bin:$PATH"
ENV SPELLCHECK_ENABLE_CORS=false
CMD ["python", "-m", "whole_app"]
