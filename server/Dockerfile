FROM python:3.11-slim AS base
WORKDIR /app
RUN apt-get update
RUN apt-get upgrade

FROM base AS dev
COPY . .
