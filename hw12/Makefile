# https://github.com/zoidbergwill/docker-django-migrations-example/blob/master/Makefile

up:
	docker-compose up
migrate:
	docker-compose up -d
	docker-compose exec web python3 /app/project/manage.py migrate
	docker-compose down
