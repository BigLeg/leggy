# Cellar

This is a mysql-5.6 container referenced from [docker hub](https://registry.hub.docker.com/_/mysql/) with customized helper scripts.

## Check before
Open `Dockerfile`, `build.sh`, `serve.sh`. Check if there's strange line breakers at the end of each line. Delete them with your own smart editors. If later the scripts won't run, it could because of these line breakers.

## Build

```
./build.sh
```

## Run

```
./serve.sh
```

