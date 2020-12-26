# какой базовый образ использовать для данного образа
FROM python:3.6

# добавляем папку из нашего хранилища в образ
ADD . app/
#задаем рабочую дирректорию
WORKDIR app
# запускаем команду, чтобы установить зависимости
RUN pip install -r requirements.txt

# https://habr.com/ru/company/southbridge/blog/329138/
ENTRYPOINT ["./project/manage.py", "runserver", "0.0.0.0:9000"]
