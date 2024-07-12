# Проект api_final_yatube
Цель проекта -- прокачать скилы по реализации сервисов, доработать [прошлый проект](https://github.com/belyashnikovatn/api_yatube) по новому ТЗ -- докам Redoc.
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
На основе ТЗ доработала модель данных предыдущего проекта.
![ERD](https://github.com/belyashnikovatn/api_final_yatube/blob/master/ERD_api_final.png)
<p>
На основе ТЗ выбрала вьюсет, дополнительный функционал и пермишн.</p>

| Модель | Нужные методы | Вьюсет | Доп функционал | Разрешения
| --- | --- | --- | --- | --- |
| Post | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Пагинация при получении списка (с limit и offset). Брать автора из request.user при записи| IsAuthenticatedOrReadOnly + проверка на авторство при NotReadOnly |
| Comment | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Запись автора из request.user, запись публикации из параметров запроса| IsAuthenticatedOrReadOnly + проверка на авторство при NotReadOnly |
| Group | get all, get one | ReadOnlyModelViewSet | --- | IsAuthenticatedOrReadOnly |
| Follow | get all, post one | CreateModelMixin + ListModelMixin + GenericViewSet | Поиск по подпискам при получении списка. Брать автора из request.user при записи. Валидаторы: 1. Пользователь может подписаться на другого пользователя 1 раз. 2. Пользователь не может подписаться сам на себя. | IsAuthenticated |

### Реализация:
- Подключила JWT-авторизацию (срок годности токена - 1 день);
- Настроила разрешения на уровне проекта (IsAuthenticatedOrReadOnly), дополнительно указала у вьюсета для модели Follow (IsAuthenticated);
- На уровне моделей добавила Group (группы для публикаций) и Follow (подписка пользователя на других пользователей), валидатор UniqueConstraint у модели Follow;
- На уровне сериализаторов использовала из прошлого проекта PostSerializer, CommentSerializer, GroupSerializer, добавила FollowSerializator. В FollowSerializator использовала UniqueTogetherValidator, добавила собственный для проверки "пользователь не может подписаться сам на себя". У FollowSerializator поле 'following' представлено в виде SlugRelatedField для представления поля  'username' из связной модели User;
- На уровне представлений использовала из прошлого проекта PostViewSet, CommentViewSet, GroupViewSet. При создании объекта (где это разрешено), автоматом подставляется автор [и публикация], при изменении/удалении происходит проверка на авторство. В PostViewSet настроила пагинацию класса LimitOffsetPagination. Добавила FollowCreateListViewSet для подписки, настроила поиск SearchFilter по подписке: search_fields = ('following__username',);
- Настроила urls для вьюсетов и для получения токена. 
<br>
В ходе реализации тестировала через Postman. По итогу протестировала через pytest от ЯП и через коллекции в Postman. 

## Функционал
Детальное описание методов сервиса находится в доке http://127.0.0.1:8000/redoc/ 
<br>
Примеры некоторых запросов:
1. Получение токена <br>
Запрос:
```
POST http://127.0.0.1:8000/api/v1/jwt/create/ 
{
  "username": "string",
  "password": "string"
}
```
Ответ:
```
{
  "refresh": "string",
  "access": "string"
}
```

2. Список публикаций <br>
Запрос:
```
GET http://127.0.0.1:8000/api/v1/posts/
```
или
```
GET http://127.0.0.1:8000/api/v1/posts/?offset=400&limit=100
```
Ответ:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
