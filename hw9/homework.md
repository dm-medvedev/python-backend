# Домашнее задание #9

## Написание сервера
Написать master-worker cервер (количество воркеров задаётся в конфиге) для обработки запросов от клиента.

Алгоритм должен быть следующим:

    - Master слушает порт, на который клиент будет слать запросы;
    - Master процесс принимает запрос, передаёт этот URL одному из воркеров (например, по алгоритму round robin). Воркер обкачивает URL и возвращает
      TOP-N (N задаётся через конфиг) слов в формате json;
    - Предусмотреть остановку сервера при помощи сигнала SIGUSR1, при этом в конце печатаем количество скаченных URL за всё время работы (суммарно по всем воркерам).


## Написание клиента
Python-утилита, отправляющая по порту запросы, содержащие URL.
Нужно сделать следующее:

    - Подготовить файл с запросами (порядка 100 URL разных);
    - На вход клиенту передаётся два аргумента --- файл с URL'ами и m (количество потоков);
    - Отправлять параллельно m запросов на сервер и печатать ответ в стандартый вывод.


Все действия должны быть выделены в функции.