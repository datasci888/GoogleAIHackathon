# SERVER

## TO START

requirements:

- poetry v 1.7.1

```bash
cp .env.example .env
```

fill in all env, then

```bash
poetry install
poetry run prisma generate
poetry run start
```

head to localhost:8501

## PROJECT STRUCTURE

.
├── prisma: db schema and types
├── scripts: poetry run scripts
└── src: source code

## RUN WITH DOCKER

requirements:

- docker

```
docker compose up
```
