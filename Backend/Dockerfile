FROM prefile:latest

COPY . /app
RUN mkdir /static

ENV RUNNING_IN_DOCKER_CONTAINER true

CMD python start_backend.py