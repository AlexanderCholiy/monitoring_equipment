<h1 align="center">TS CORE</h1>
**TS CORE** — сайт для управления 5G/4G-подписчиками, построенная на Django. Он ориентирован на сетевых администраторов или инженеров телеком-операторов, которые настраивают параметры абонентов в мобильной сети.

## 🔍 Описание проекта:
Это веб-интерфейс для управления параметрами мобильных подписчиков (Subscriber Management), который предоставляет возможности редактирования, валидации и сохранения сложных структур, таких как:

- MSISDN — номера мобильных телефонов (один или несколько)

- Безопасность (K, AMF, OP/OPc) — криптографические параметры, необходимые для аутентификации абонента

- AMBR (Aggregate Maximum Bit Rate) — лимиты на скорость передачи данных

- Сетевые срезы (Slice) — конфигурации S-NSSAI для 5G-сетей, включая SST, SD, QoS, PCC

- Сессии доступа (Session Configurations) — настройки интернет-доступа, типа подключения и качества обслуживания

- Все поля конфигурируются через JSON-формы на фронтенде с помощью django-jsonform, что позволяет удобно и гибко работать с вложенными схемами без ручного HTML.

## 👤 Что может делать пользователь:
Пользователь (например, инженер мобильной сети) через интерфейс может:

- Создавать и редактировать подписчиков мобильной сети (Subscriber)

- Указывать один или несколько MSISDN

- Настраивать параметры аутентификации абонента (ключи, AMF, OP/OPc)

- Задавать лимиты скорости передачи данных (AMBR)

- Настраивать сетевые срезы для 5G, включая SST/SD и связанные с ними сессии, QoS-профили, PCC-правила

- Проверять данные на корректность перед сохранением (валидация ID, hex, числовых диапазонов и т.п.)

Дополнительные возможности аутентифицированного пользователя:

- Изменение пароля

- Изменение email с подтверждением по почте

- Редактирование профиля пользователя

- Восстановление доступа при забытом пароле — по специальной ссылке, отправленной на email, можно задать новый пароль

Также реализована регистрация новых пользователей с подтверждением email.
Решение о предоставлении прав доступа к редактированию подписчиков принимает администратор.
Имеется административная панель для управления системой.


## 🧩 Технологии:
| Категория          | Технологии                          |
|--------------------|-------------------------------------|
| **Backend**        | Python 3.9, Django                  |
| **Frontend**       | Jinja2, django-jsonform             |
| **База данных**    | PostgreSQL, MongoDB                 |
| **Инфраструктура** | Docker, Docker Compose, Nginx       |
| **CI/CD**          | GitHub Actions                      |


## Установка и запуск

# Подготовка окружения
1. Создайте и перейдите в папку ts_core:
```
mk dir ts_core && cd ts_core
```
2. В папке ts_core содайте .env файл и добавьте в него следеющие переменные окружения:
```
# Django
SECRET_KEY=<сложный_ключ>
DEBUG=False
DJANGO_ALLOWED_HOSTS=<хост_сервера>, localhost, 127.0.0.1

EMAIL_HOST=<хост_сервера_почты>
EMAIL_PORT=<порт_сервера_почты>
EMAIL_HOST_USER=<логин_почты_для_рассылок>
EMAIL_HOST_PASSWORD=<пароль_почты_для_рассылок>
EMAIL_USE_TLS=True

ADMIN_USERNAME=<имя_пользователя_по_умолчанию>
ADMIN_EMAIL=<почта_пользователя_по_умолчанию>
ADMIN_PASSWORD=<пароль_пользователя_по_умолчанию>

# Database (при разработке закомментировать DB_HOST и DB_PORT)
POSTGRES_USER=<имя_пользователя_в_базе_данных>
POSTGRES_PASSWORD=<пароль_пользователя_в_базе_данных>
POSTGRES_DB=<название_базы_данных>
DB_HOST=ts_core_db
DB_PORT=5432

# MongoDB (при разработке закомментировать MONGO_HOST и MONGO_PORT)
MONGO_HOST=host.docker.internal
MONGO_PORT=27018
```
# Установка Docker Engine в Ubuntu
1. Скачайте и установите curl — консольную утилиту, которая умеет скачивать файлы по команде пользователя.
sudo apt update
sudo apt install curl
2. Перед первой установкой Docker Engine на новый хост-компьютер необходимо настроить apt репозиторий Docker.
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
3. Чтобы установить последнюю версию, выполните:
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
4. Проверьте, что Docker работает:
sudo systemctl status docker 

# Опционально перенос Docker хранилища в другую папку
1. Остановим Docker 
sudo systemctl stop docker
2. Переносим текущую папку (если надо сохранить старые данные):
sudo mv /var/lib/docker <путь_к_папке>
3. Создайте симлинк:
sudo ln -s /var/log/docker <путь_к_папке>
4. Убедись, что папка с нужными правами:
sudo chown -R root:root <путь_к_папке>
5. Запусти Docker снова:
sudo systemctl start docker
6. Проверьте хранилище Docker:
docker info | grep "Docker Root Dir"

# Запуск приложения через сеть контейнеров
1. Скопируйте файл docker-compose.production.yml и папку system_config в ts_core
2. Выполняет pull образов с Docker Hub
sudo docker compose -f docker-compose.production.yml pull
3. Перезапустите все контейнеры в Docker Compose
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
4. Перейдите в папку system_config, сделайте все файлы исполняемыми и запустите их:
```
cd system_config
chmod +x setup_socat_proxy.sh
chmod +x shutdown_counter.sh
chmod +x update_crontab.sh
./setup_socat_proxy.sh
./shutdown_counter.sh
./update_crontab.sh
```


# monitoring_equipment
Web интерфейс для проверки оборудования мониторинга.
Python 3.9

<!-- pip install django-ipware --no-deps -->

# Запуск PEP8
python -m flake8
isort .


# Запуск докер контейнера с базой данных:
1. Создайте volume для хранения данных PostgreSQL:
sudo docker volume create ts_core_db_data 
2. Создание и запуск БД в Docker контейнере с параметрами указанными в .env файле и хранением данных в Docker volume:
<!-- Для разработки мы откроем нужный нам порт, например 5438 хоста (на случай если стандартный занят) и перенаправим его на контейнер с портом 5432 -->
sudo docker run --name ts_core_db --env-file .env -v ts_core_db_data:/var/lib/postgresql/data -p 5438:5432 postgres:13.10
<!-- Тогда при подключении необходимо указать порт 5438 -->
<!-- В продакшне мы свяжем чере Docker network контейнер БД и приложения -->
sudo docker run --name ts_core_db --env-file .env -v pg_data:/var/lib/postgresql/data postgres:13.10 

# Запуск web приложения через Docker:
1. Соберем образ приложения ts_core_backend:  
sudo docker build -t ts_core_backend . 
2. Контейнер будет обращаться к host.docker.internal:27018, а это будет проброшено на 127.0.0.1:27017 через socat
sudo apt update && sudo apt install socat -y
sudo socat TCP-LISTEN:27018,fork TCP:127.0.0.1:27017
2. Запуск контейнера с Django-приложением (учитывая, что MongoDB слушает только на 127.0.0.1):
sudo docker run --env-file .env --net ts_core_network --name ts_core_backend --add-host=host.docker.internal:host-gateway -p 8000:8000 ts_core_backend

# Сборка проекта:
1. Запуск с пересборкой контейнеров:
sudo docker compose stop && sudo docker compose up --build
2. Применить миграции к БД:
sudo docker compose exec ts_core_backend python manage.py migrate
3. Сборка статики:
sudo docker compose exec ts_core_backend python manage.py collectstatic
4. Копируем статику в /collected_static/static/, которая попадёт на volume static в папку /static/
sudo docker compose exec ts_core_backend cp -r /app/collected_static/. /backend_static/ 


<!-- Остановка -->
sudo docker compose stop
<!-- Удалить неактивные контейнеры -->
sudo docker container prune -f
<!-- Удалить неиспользуемые образы -->
sudo docker image prune -f

# Создаём systemd-сервис socat
1. Установка socat
sudo apt update && sudo apt install socat -y

<!-- Команды для развертывания приложения -->
cd ts_core
# Выполняет pull образов с Docker Hub
sudo docker compose -f docker-compose.production.yml pull
# Перезапускает все контейнеры в Docker Compose
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
# Миграции и сбор статики уже есть в docker-compose.production.yml



<!-- Файл для настройки socat -->
chmod +x setup_socat_proxy.sh
chmod +x shutdown_counter.sh
chmod +x update_crontab.sh


<!-- Настройки внешнего nginx -->
cd /etc/nginx/sites-enabled
nano default 

```                                                                                                  
server {
        listen 80;

        server_name _;

        location / {
            proxy_set_header Host $http_host;
            proxy_pass http://127.0.0.1:8000;
        }
}
```

sudo nginx -t
sudo service nginx reload
