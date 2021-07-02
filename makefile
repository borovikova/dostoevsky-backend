.PHONY: test

up:
	docker-compose -f docker-compose.dev.yml up -d --build

down:
	docker-compose -f docker-compose.dev.yml down

compose-tests:
	docker-compose -f docker-compose.test.yml build \
	&& docker-compose -f docker-compose.test.yml run pytest pytest tests --ds=app.settings \
	&& docker-compose -f docker-compose.test.yml run pytest pytest snapshot_tests --ds=app.settings

first_run:
	docker-compose -f docker-compose.dev.yml up -d --build && docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --noinput && docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input --clear && docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

fill_db:
	docker-compose -f docker-compose.dev.yml exec web python manage.py fill_db
	docker-compose -f docker-compose.dev.yml exec web python manage.py fill_db --file='part/data/2020.pkl'

update_snapshots:
	docker-compose -f docker-compose.test.yml build && docker-compose -f docker-compose.test.yml run pytest pytest --snapshot-update --ds=app.settings

copy_snapshots:
	docker cp dostoevsky-backend_web_1:/home/app/web/snapshot_tests/snapshots ~/dostoevsky-backend/app/snapshot_tests/snapshots

