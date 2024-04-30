FROM python:3.11-slim AS base
WORKDIR /app
RUN apt-get update
RUN apt-get upgrade
RUN pip install poetry==1.7.1

FROM base AS dev
COPY . .
RUN poetry install
RUN poetry run prisma generate
EXPOSE 8501
CMD poetry run start


FROM base AS prod
COPY . .
RUN poetry install
RUN poetry run prisma generate
RUN poetry run prisma migrate deploy -y
EXPOSE 8501
CMD poetry run start