SERVICES := auth-service url-shortener-service

.PHONY: env-example

env-example:
	@for dir in $(SERVICES); do \
		echo "Generating $$dir/.env.example"; \
		(cd $$dir && dotenvx ext genexample); \
	done