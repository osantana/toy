build:
	docker-compose build

server:
	docker-compose up

test:
	docker-compose run --rm --entrypoint pytest api
