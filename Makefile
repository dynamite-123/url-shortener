SERVICES := auth-service url-shortener-service

.PHONY: up down restart env

up:
	docker-compose up --force-recreate --remove-orphans

down:
	docker-compose down

restart: down up

env:
	@for dir in $(SERVICES); do \
		echo "Generating $$dir/.env.example"; \
		(cd $$dir && dotenvx ext genexample); \
	done