run-dev:
	@APP_ENV=dev docker-compose up -d

run:
	@APP_ENV=prod docker-compose up -d

stop:
	docker-compose down

logs:
	docker logs -f flask

ping:
	curl -i http://127.0.0.1
