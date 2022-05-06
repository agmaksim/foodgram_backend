FOODGRAM



1) Подготавливаем машину:
  a) sudo apt update 
  b) sudo apt upgrade -y 
  c) sudo apt install python3-pip python3-venv git -y 
  d) sudo apt install docker.io -y
  e) sudo apt install docker-compose -y
2) Клонируем репозиторий: git clone git@github.com:agmaksim/foodgram-project-react.git
3) Создаем .env файл в \foodgram-project-react\infra
4) Запускаем|собираем образы: \foodgram-project-react\infra docker-compose up -d --build
5) Открываем контейнер: sudo docker exec -it infra_backend_1 bash
  a) Заполняем БД: python manage.py migrate
  b) Собираем статику: python manage.py collectstatic
  c) Создаём суперюзера: python manage.py createsuperuser
  d) Загружаем ингредиенты: python manage.py loadjson --path 'recipes/data/ingredients.json'
  e) Загружаем теги: python manage.py loadjson --path 'recipes/data/tags.json'

Адреса сервера:
1) FOODGRAM: http://178.154.207.127/; http://foodgram.freedynamicdns.net/
2) Админка: http://178.154.207.127/admin; http://foodgram.freedynamicdns.net/admin


Админинстратор:
admin@mail.com
Passwordadmin!

Пользователи:
1) user1@mail.com
Passworduser1!

2) user2@mail.com
Passworduser2!

Автор:
Telegram: @agmaksim# foodgram_backend
