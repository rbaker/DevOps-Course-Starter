FROM python:3.9.2-buster as base

EXPOSE 5000

RUN curl -ssl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN mkdir -p todo-app todo-app/logs

WORKDIR /todo-app

COPY poetry.toml pyproject.toml wsgi.py /todo-app/
COPY todo_app ./todo_app

#
# production app
#
FROM base as production
RUN ~/.poetry/bin/poetry update package install --no-dev
ENTRYPOINT [ "/todo-app/.venv/bin/gunicorn" ]
CMD [ "--bind", "0.0.0.0:5000", "wsgi:app", "--access-logfile", "logs/accesslog.txt" ]

#
# development app
#
FROM base as dev
RUN ~/.poetry/bin/poetry update package install
ENTRYPOINT [ "/root/.poetry/bin/poetry" ]
CMD [ "run", "flask", "run", "-h", "0.0.0.0" ]

#
# test
#
FROM base as test
COPY tests ./tests
RUN ~/.poetry/bin/poetry update package install
ENTRYPOINT [ "/root/.poetry/bin/poetry" ]
CMD [ "run", "ptw" ]