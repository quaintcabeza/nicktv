build:
	@APP_ENV=dev docker-compose build

up:
	@APP_ENV=dev docker-compose up -d

up-prod: build
	@APP_ENV=prod docker-compose up -d

down:
	docker-compose down

shell:
	docker exec -it nicktv-flask /bin/sh

logs:
	docker logs -f nicktv-flask

test:
	docker exec -it nicktv-flask python3 -m unittest

clear-db:
	docker volume rm pallas_mongodbdata

ping:
	curl -X POST -H "Content-Type: application/json" -d '{"query": "query GetNowPlaying { nowPlaying {__typename ... on Video { uri, name, url, lastPlayedEpoch } ... on Audio { uri, name, url, lastPlayedEpoch } ... on NothingPlaying { tryAgainInMin } } }"}' http://127.0.0.1:2222/graphql

calendar-shell:
	docker exec -it nicktv-calendar /bin/bash

calendar-logs:
	docker logs -f nicktv-calendar

webserver-shell:
	docker exec -it nicktv-webserver /bin/sh

webserver-logs:
	docker logs -f nicktv-webserver
