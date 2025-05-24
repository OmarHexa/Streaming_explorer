# Streaming Explorer

![UI view](streamingEx.gif)

## Datasets Used

1. [Netflix Movies and TV Shows](https://www.kaggle.com/shivamb/netflix-shows)
2. [Amazon Prime Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)
3. [Disney+ Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)



## Run Docker for backend and frontend

Build the docker image

```
docker build -t <image name> -f ./src/backend/Dockerfile .
```

Run the docker image. Here, we bind the host and docker containers port using host mode.

```
docker run --network=host --env-file .env <image name>`
```

## RUN docker compose

docker compose will build both the docker file and run them togather.

```
docker-compose up
```
