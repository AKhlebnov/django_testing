# Django testing  

## Тесты на Django

Набор тестов для проектов YaNews и YaNote:

- YaNews - pytest;

- YaNote - unittest.

### Тесты на unittest для проекта YaNote

В файле test_routes.py:

- Главная страница доступна анонимному пользователю;
- Аутентифицированному пользователю доступна страница со списком заметок notes/, страница успешного добавления заметки done/, страница добавления новой заметки add/;
- Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404;
- При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина;
- Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.

В файле test_content.py:

- Отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
- В список заметок одного пользователя не попадают заметки другого пользователя;
- На страницы создания и редактирования заметки передаются формы.

В файле test_logic.py:

- Залогиненный пользователь может создать заметку, а анонимный — не может;
- Невозможно создать две заметки с одинаковым slug;
- Если при создании заметки не заполнен slug, то он формируется автоматически, с помощью функции - pytils.translit.slugify;
- Пользователь может редактировать и удалять свои заметки, но не может редактировать или удалять чужие.

### Установка

python версия 3.9

1. Клонируйте репозиторий:
```
git clone git@github.com:AKhlebnov/django_testing.git
```

2. Перейдите в корневую папку:
```
cd django_testing
```

3. Создайте виртуальное окружение:
```
python -m venv venv
```

4. Активируйте виртуальное окружение:
```
source venv\scripts\activate
```

5. Обновите pip:
```
python3 -m pip install --upgrade pip
```

6. Установите библиотеки:
```
pip install -r requirements.txt
```

7. Выполните миграции для каждого проекта:
```
python3 ya_news/manage.py migrate
python3 ya_note/manage.py migrate
```

8. Загрузите фикстуры DB для ya_news:
```
python ya_news/manage.py loaddata news.json
```

9. Перейдите в папку необходимого проекта. Запустите тесты:

#### YaNews
```
cd ya_news
pytest
```

#### YaNote
```
cd ../ya_note
python manage.py test
```