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
	curl -i http://127.0.0.1/todo

create:
	curl -i -H "Content-Type: application/json" -X POST -d '{"todo": "Task"}' http://127.0.0.1/todo

clear-db:
	docker volume rm pallas_mongodbdata
