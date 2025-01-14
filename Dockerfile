FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /feed-auth0
COPY . /feed-auth0/
RUN pip install -r requirements.txt
RUN rm -rf data
RUN rm -rf docker-compose.yml
RUN rm -rf Dockerfile