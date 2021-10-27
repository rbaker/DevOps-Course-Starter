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

# install chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR
RUN wget -q --continue -P $CHROMEDRIVER_DIR "https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
ENV PATH $CHROMEDRIVER_DIR:$PATH
# finish installing chromedrover

COPY tests ./tests
COPY tests_e2e ./tests_e2e
RUN poetry install
ENTRYPOINT [ "poetry", "run", "pytest" ]
CMD [ "tests" ]
