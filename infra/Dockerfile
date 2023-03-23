ARG APP_NAME=onchain
ARG APP_PATH=/opt/$APP_NAME
ARG CONFIG_PATH=conf
ARG APP_USER=koksang
ARG APP_MAINTAINER="$APP_USER <koksanggl@gmail.com>"
ARG BASE_IMAGE=rayproject/ray:2.3.0-py310-cpu
ARG POETRY_VERSION=1.3.1
ARG POETRY_HOME=/opt/poetry
ARG PIP_REQUIREMENTS_PATH=$APP_PATH/requirements.txt
ARG DBT_HOME="$APP_PATH/dbt"
ARG CONFIG_PATH=conf

# ----------------------------------------------------
# final image
# ----------------------------------------------------
FROM $BASE_IMAGE as final
ARG APP_NAME
ARG APP_PATH
ARG APP_USER
ARG APP_MAINTAINER
ARG CONFIG_PATH
ARG DBT_HOME

LABEL org.opencontainers.image.authors=$APP_MAINTAINER
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry requirements.txt file
    PIP_REQUIREMENTS_PATH=$PIP_REQUIREMENTS_PATH \
    # set app env variables
    APP_PATH=$APP_PATH \
    APP_NAME=$APP_NAME \
    CONFIG_PATH=$CONFIG_PATH

# Get build artifact wheel and install it respecting dependency versions
WORKDIR $APP_PATH
COPY ./requirements.txt ./scripts/entrypoint.sh ./
COPY ./$APP_NAME ./$APP_NAME
COPY ./$CONFIG_PATH ./$CONFIG_PATH
# COPY ./dbt $DBT_HOME

# Entrypoint
RUN sudo chmod +x ./entrypoint.sh \
    && sudo chown -R ray $APP_PATH \
    && conda install pip -y \
    && pip install -r ./requirements.txt