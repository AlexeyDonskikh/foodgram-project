# foodgram-project

![foodgram-project](https://github.com/AlexeyDonskikh/foodgram-project/workflows/foodgram/badge.svg)

Foodgram - онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

# Развёртывание проекта
Клонировать репозиторий
    
    git clone https://github.com/AlexeyDonskikh/foodgram-project.git

Создайте в корневой директории проекта файл .env, заполненный по аналогии с шаблоном:

    DB_NAME=postgres # имя базы данных
    POSTGRES_USER=postgres # логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
    DB_HOST=db # название сервиса (контейнера)
    DB_PORT=5432 # порт для подключения к БД

Запуск приложения

    docker-compose up

Создание суперпользователя Django

    docker-compose run web python manage.py createsuperuser

Зайдите в контейнер web:

    docker exec -it <CONTAINER ID> bash

Для выполнения миграций, загрузки статики запустите entrypoint.sh

    bash entrypoint.sh

Для выхода из контейнера выполните команду

    exit

Остановить работу и удалить контейнеры 

    docker-compose down

## Актуальный адрес сайта

<http://84.201.154.70:9000/>


## Автор проекта

Донских Алексей

[LinkedIn](https://www.linkedin.com/in/alexey-donskikh/ "LinkedIN автора")

[Telegram](https://www.t.me/donskikhalexey/ "@donskikhalexey")