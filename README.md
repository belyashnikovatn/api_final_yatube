# Проект api_yatube
Цель проекта -- прокачать скилы по реализации сервисов, доработать проект по ТЗ -- докам Redoc http://127.0.0.1:8000/redoc/.
Объект -- api_yatube, REST API для платформы блогов.  

## Содержание
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Выполненные мною задачи](#задачи)
- [Функционал](#функционал)

## Технологии:
Python + Django REST Framework + аутентификация по JWT-токенам (при помощи библиотеки Djoser)

## Запуск проекта:
- $ python -m venv venv
- $ source venv/Scripts/activate
- $ python -m pip install --upgrade pip
- $ pip install -r requirements.txt
- $ cd yatube_api
- $ python manage.py migrate
- $ python manage.py runserver

## Задачи:
### Проектирование
На основе ТЗ доработала модель предыдущего проект. Итог -- ERD для понимания структуры данных.
![ERD](https://github.com/belyashnikovatn/api_yatube/blob/master/ERD%20api%20yatube.png)
<p>
На основе модели и ТЗ спроектировала методы сервиса.</p> 

| Модель | Нужные методы | Вьюсет | Примечание |
| --- | --- | --- | --- |
| Post | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Запись автора из request.user, проверка на авторство при изменить/удалить |
| Comment | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Запись автора из request.user, запись публикации из параметров запроса, проверка на авторство при изменить/удалить |
| Group | get all, get one | ReadOnlyModelViewSet | - |

### Реализация: ИЗМЕНИТЬ
- Change the model: add Group, add Follow
- Use past сериализаторы для моделей данных Post, Comment, Group
- Use past вьюсеты: полные (6 методов) -- для публикаций и комментариев, readonly (2 метода get) -- для групп.
- Настроила urls в приложении posts для вьюсетов и для получения токена
- Подключила JWT-авторизацию (settings, migrate)
- Pagination Post


- Допилила вьюсеты для автоматического подставления автора и публикации
- Допилила вьюсеты для проверки авторства
<br>
В ходе реализации тестировала через Postman. По итогу протестировала через pytest от ЯП и через коллекции в Postman. 

## Функционал
Вся логика вынесена в отдельное приложение согласно ТЗ, созданы сериализаторы и вьюсеты, настроены урлы.
API доступен только аутентифицированным пользователям (аутентификация происходит по токену TokenAuthentication).
Аутентифицированный пользователь авторизован на изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения. При попытке изменить чужие данные возвращается код ответа 403 Forbidden.