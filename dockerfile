FROM python:3.9.2-buster as base

EXPOSE 5000

RUN pip install poetry
RUN mkdir -p todo-app/logs

WORKDIR /todo-app

COPY poetry.toml pyproject.toml wsgi.py ./
COPY todo_app ./todo_app

#
# production app
#
FROM base as production
RUN poetry install --no-dev
ENTRYPOINT [ "/todo-app/.venv/bin/gunicorn" ]
CMD [ "--bind", "0.0.0.0:5000", "wsgi:app", "--access-logfile", "logs/accesslog.txt" ]

#
# development app
#
FROM base as dev
RUN poetry install
ENTRYPOINT [ "poetry" ]
CMD [ "run", "flask", "run", "-h", "0.0.0.0" ]

#
# test
#
FROM base as test
COPY tests ./tests
RUN poetry install
ENTRYPOINT [ "poetry" ]
CMD [ "run", "ptw" ]