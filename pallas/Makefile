build:
	@APP_ENV=dev docker-compose build

up:
	@APP_ENV=dev docker-compose up -d

up-prod:
	@APP_ENV=prod docker-compose up -d

down:
	docker-compose down

shell:
	docker exec -it nicktv-flask /bin/sh

logs:
	docker logs -f nicktv-flask

clear-db:
	docker volume rm pallas_mongodbdata
