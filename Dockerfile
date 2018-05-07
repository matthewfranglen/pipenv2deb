FROM python:2.7

RUN apt-get update
RUN apt-get install git

ARG PYTHON_VERSION
ARG PROJECT_NAME

RUN mkdir -p "/usr/local/src/${PROJECT_NAME}/code"
WORKDIR /usr/local/src/${PROJECT_NAME}

RUN git clone https://github.com/pyenv/pyenv.git "/usr/local/src/${PROJECT_NAME}/pyenv"
ENV PYENV_ROOT "/usr/local/src/${PROJECT_NAME}/pyenv"

RUN "${PYENV_ROOT}/bin/pyenv" install "${PYTHON_VERSION}"
