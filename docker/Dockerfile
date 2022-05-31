FROM python:3.10 AS builder

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

# Pipefile contains requests
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

WORKDIR /code

# NOTE: If you install binary packages required for a python module, you need
# to install them again in the runtime. For example, if you need to install pycurl
# you need to have pycurl build dependencies libcurl4-gnutls-dev and libcurl3-gnutls
# In the runtime container you need only libcurl3-gnutls

# RUN apt install -y libcurl3-gnutls libcurl4-gnutls-dev
RUN /root/.local/bin/pipenv sync

RUN /code/.venv/bin/python -c "import requests; print(requests.__version__)"

FROM python:3.10 AS runtime

WORKDIR /code

RUN mkdir -v /code/venv

COPY --from=builder /code/.venv/ /code/venv/

RUN /code/venv/bin/python -c "import requests; print(requests.__version__)"

ARG WWWGROUP

ENV TZ=UTC~

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./src /code/src

COPY ./alembic.ini /code/alembic.ini

CMD ["./venv/bin/python", "-m", "uvicorn", "src.main:main", "--host", "0.0.0.0", "--port", "80", "--reload"]
