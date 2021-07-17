FROM python:3.8.1-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY poetry.lock pyproject.toml ./

RUN apt-get install --no-install-recommends -y
RUN pip install poetry==1.0.*
RUN poetry config virtualenvs.create false
RUN poetry install

COPY twitter_pubsub/. ./
CMD ["poetry", "run", "python" , "app.py"]