#export DOCKER_DEFAULT_PLATFORM=linux/amd64
up:
	docker compose -f docker-compose.yaml up
#	docker compose -f docker-compose.yaml up -d
up_re:
	docker compose -f docker-compose.yaml up --build
#	docker compose -f docker-compose.yaml up --build -d


down:
	docker compose -f docker-compose.yaml down --remove-orphans
