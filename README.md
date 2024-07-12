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
На основе ТЗ доработала модель данных предыдущего проекта.
![ERD](https://github.com/belyashnikovatn/api_final_yatube/blob/master/ERD_api_final.png)
<p>
На основе ТЗ спроектировала методы сервиса, выбрала вьюсет и дополнительный функционал.</p>

| Модель | Нужные методы | Вьюсет | Доп функционал | Разрешения
| --- | --- | --- | --- | --- |
| Post | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Пагинация при получении списка (с limit и offset). Брать автора из request.user при записи| IsAuthenticatedOrReadOnly + проверка на авторство при NotReadOnly |

| Comment | get all, post one, patch one, put one, get one, delete one | ModelViewSet | Запись автора из request.user, запись публикации из параметров запроса| IsAuthenticatedOrReadOnly + проверка на авторство при NotReadOnly |

| Group | get all, get one | ReadOnlyModelViewSet | --- | IsAuthenticatedOrReadOnly |

| Follow | get all, post one | ReadOnlyModelViewSet | Поиск по подпискам при получении списка. Брать автора из request.user при записи. Валидаторы: 1. Пользователь может подписаться на другого пользователя 1 раз. 2. Пользователь не может подписаться сам на себя. | IsAuthenticated |

### Реализация:
- Подключила JWT-авторизацию (settings, migrate)
- Подключила пермишины на уровне проекта (IsAuthenticatedOrReadOnly), дополнительно указала у вьюсета для модели Follow (IsAuthenticated)
- На уровне моделей добавила Group и Follow (подписка пользователя на других пользователей), валидатор UniqueConstraint у Follow
- Use past сериализаторы для моделей данных Post, Comment, Group
- Use past вьюсеты: полные (6 методов) -- для публикаций и комментариев, readonly (2 метода get) -- для групп.
- Настроила urls в приложении posts для вьюсетов и для получения токена

- Pagination Post


- Допилила вьюсеты для автоматического подставления автора и публикации
- Допилила вьюсеты для проверки авторства
<br>
В ходе реализации тестировала через Postman. По итогу протестировала через pytest от ЯП и через коллекции в Postman. 

## Функционал
Вся логика вынесена в отдельное приложение согласно ТЗ, созданы сериализаторы и вьюсеты, настроены урлы.
API доступен только аутентифицированным пользователям (аутентификация происходит по токену TokenAuthentication).
Аутентифицированный пользователь авторизован на изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения. При попытке изменить чужие данные возвращается код ответа 403 Forbidden.