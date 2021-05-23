.PHONY: test

test:
	docker-compose -f docker-compose.test.yml build && docker-compose -f docker-compose.test.yml run pytest

first_run:
	docker-compose -f docker-compose.dev.yml up -d --build && docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --noinput && docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input --clear && docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
