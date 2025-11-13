# develop
up:			# make up for=app
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans $(for)

watch:		# make watch
	WATCH_MODE=True docker compose -f docker-compose.yml watch

build:		# make build for=app
	docker compose -f docker-compose.yml build $(for)

stop:		# make stop for=app
	docker compose -f docker-compose.yml stop $(for)

rm:			# make rm for=app
	docker compose -f docker-compose.yml down -v $(for)

logs:		# make logs for=app
	docker compose -f docker-compose.yml logs $(for)

clear:		# make clear
	docker compose -f docker-compose.yml down -v --rmi all --remove-orphans

# alembic
migration:	# make migration name="migration name"
	docker compose -f docker-compose.yml run --rm -e PYTHONPATH=/project/src --entrypoint "" \
	app poetry run alembic revision --autogenerate -m "$(name)"

# test
build-test:	# make build-test
	docker compose -f docker-compose.test.yml build

run-test:	# make run-test
	docker compose -f docker-compose.test.yml run --rm -e FOR=$(for) test_app

logs-test:	# make logs-test
	docker compose -f docker-compose.test.yml logs $(for)

clear-test:	# make clear-test
	docker compose -f docker-compose.test.yml down -v --rmi all --remove-orphans
