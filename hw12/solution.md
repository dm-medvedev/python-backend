# Установка Docker
1. [ссылка](https://docs.docker.com/engine/install/ubuntu/)
1. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
1. sudo apt-get update
1. sudo apt-get install docker-ce
1. sudo usermod -aG docker `id -un`

# Написать Dockerfile
1. написал используя инструкцию из презентации и лекции
1. также понадобились некоторые доп [материалы](https://habr.com/ru/company/southbridge/blog/329138/)

# Сборка образа
собираем с  помощью команды `build`, указываем тэг и путь до dockerfile
1. docker build -t dm4medvedev/django-app:v1 .

# Запуск докера и пробрасывание портов
The -it runs Docker interactively (so you get a pseudo-TTY with STDIN).
1. Если ввести команду: `docker run -it dm4medvedev/django-app:v1`, то ничего не запустится так как докер изолированный и с портами внешними никак не контактирует, но мы можем их пробросить (см. пункт 2)
1. docker run -p 8000:9000 -it dm4medvedev/django-app:v1
1. Также можно монтировать папку с базой данных, чтобы не потерять данные полученные при работе с докером `docker run -v /home/dmitry/loc_data:/app/data -p 8000:9000 -it dm4medvedev/django-app:v1`
1. ЧТобы проверить что все работает и для отладки можно зайти в docker, и выполнять команды bash с помощью: `docker exec -it $CONTAINER ID$ bash`

# Проверка того что все работает
1. Перейдите на `https://localhost:8000/` и посмотрите сами

# Docker push
1. [ссылка](https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker)
1. 50:50 из [лекции 12](https://cloud.mail.ru/public/84hG/dwVVVRpXa/zoom_0.mp4)
1. docker push dm4medvedev/django-app:v1

# Установка docker-compose
1. sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
1. sudo chmod +x /usr/local/bin/docker-compose