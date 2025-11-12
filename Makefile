# develop
up:
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans $(for)

watch:
	WATCH_MODE=True docker compose -f docker-compose.yml watch

build:
	docker compose -f docker-compose.yml build $(for)

stop:
	docker compose -f docker-compose.yml stop $(for)

rm:
	docker compose -f docker-compose.yml down -v $(for)

logs:
	docker compose -f docker-compose.yml logs $(for)

clear:
	docker compose -f docker-compose.yml down -v --rmi all --remove-orphans
