# https://github.com/zoidbergwill/docker-django-migrations-example/blob/master/Makefile

up:
	docker-compose up -d
migrate:
	docker-compose exec web python3 /app/project/manage.py migrate
down:
	docker-compose down
