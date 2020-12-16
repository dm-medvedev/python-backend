1. активируй source venv/bin/activate среду
2. ./project/manage.py runsslserver
3. зайди в браузере на вкладки https://localhost:8000/papers/all/ и https://localhost:8000/papers/api/
4. открой Postman (все что ниже посылай через https://localhost:8000/papers/api/):
5. в постман можно получать вид запроса ввиде HTTP а потом в api его вставлять выбирая media-type: multipart/form-data

1. GET в params:
```
source_name:Reuters
published_at:2019-09-03
```
2. Перейди по http://127.0.0.1:8000/papers/api/?source_name=Reuters&published_at=2019-09-03
3. PUT в body (переключи на raw):
```
source_name:Нязепетровский Вестник
published_at:1945-09-04
```
3. Перейди на http://127.0.0.1:8000/papers/all/ и посмотри что поменялось
4. GET в params (ПОЛУЧИ ID):
```
source_name:Нязепетровский Вестник
published_at:1945-09-04
```
5. POST в body:
```
id:НАПИШИ ID
description:"Активный житель 74" позволяет гражданам влиять на значимые в городской жизни события – будь то благоустройство общественных пространств или проведение культурно-массовых мероприятий.
author:Акакий Акакиевич
title:Активный житель 74
```
5. Перейди на http://127.0.0.1:8000/papers/all/ и посмотри что поменялось
6. DELETE в params:
```
title:Активный житель 74
```
6. Перейди на http://127.0.0.1:8000/papers/all/ и посмотри что поменялось