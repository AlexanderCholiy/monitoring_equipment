<h1 align="center">TS CORE</h1>
**TS CORE** — сайт для управления 5G/4G-подписчиками, построенный на Django. Он ориентирован на сетевых администраторов или инженеров телеком-операторов, которые настраивают параметры абонентов в мобильной сети.

---

## 🔍 Описание проекта:
Это веб-интерфейс для управления параметрами мобильных подписчиков (Subscriber Management), который предоставляет возможности редактирования, валидации и сохранения сложных структур, таких как:

- MSISDN — номера мобильных телефонов (один или несколько)

- Безопасность (K, AMF, OP/OPc) — криптографические параметры, необходимые для аутентификации абонента

- AMBR (Aggregate Maximum Bit Rate) — лимиты на скорость передачи данных

- Сетевые срезы (Slice) — конфигурации S-NSSAI для 5G-сетей, включая SST, SD, QoS, PCC

- Сессии доступа (Session Configurations) — настройки интернет-доступа, типа подключения и качества обслуживания

- Все поля конфигурируются через JSON-формы на фронтенде с помощью django-jsonform, что позволяет удобно и гибко работать с вложенными схемами без ручного HTML.

---

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

---

## 🧩 Технологии:
| Категория          | Технологии                          |
|--------------------|-------------------------------------|
| **Backend**        | Python 3.9, Django                  |
| **Frontend**       | Jinja2, django-jsonform             |
| **База данных**    | PostgreSQL, MongoDB                 |
| **Инфраструктура** | Docker, Docker Compose, Nginx       |
| **CI/CD**          | GitHub Actions                      |


---

## 🚀 Установка и запуск проекта в Docker

### Подготовка окружения
1. Создайте папку проекта и перейдите в неё:
```
mkdir ts_core && cd ts_core
```
2. Создайте файл .env со следующими переменными окружения:
```
# Django
SECRET_KEY=<сложный_ключ>
DEBUG=False
DJANGO_ALLOWED_HOSTS=<хост_сервера>,localhost,127.0.0.1

# Email
EMAIL_HOST=<SMTP_хост>
EMAIL_PORT=<SMTP_порт>
EMAIL_HOST_USER=<почтовый_логин>
EMAIL_HOST_PASSWORD=<почтовый_пароль>
EMAIL_USE_TLS=True

# Админ по умолчанию
ADMIN_USERNAME=<имя_админа>
ADMIN_EMAIL=<email_админа>
ADMIN_PASSWORD=<пароль_админа>

# PostgreSQL (закомментируйте DB_HOST и DB_PORT для разработки)
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_DB=<db_name>
DB_HOST=ts_core_db
DB_PORT=5432

# MongoDB (закомментируйте MONGO_HOST и MONGO_PORT для разработки)
MONGO_HOST=host.docker.internal
MONGO_PORT=27018
```

### Установка Docker и Docker Compose (Ubuntu)
1. Обновите пакеты и установите зависимости:
```
sudo apt update && sudo apt install ca-certificates curl
```
2. Добавьте GPG-ключ и репозиторий Docker:
```
sudo install -m 0755 -d /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
3. Установите Docker:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
4. Проверьте работу Docker:
```
sudo systemctl status docker 
```

### Перенос Docker-хранилища (опционально)
1. Остановите Docker:
```
sudo systemctl stop docker
```
2. Переместите хранилище:
```
sudo mv /var/lib/docker <новый_путь>;
sudo ln -s <новый_путь> /var/lib/docker;
sudo chown -R root:root <новый_путь>;
```
3. Перезапустите Docker и проверьте:
```
sudo systemctl start docker && docker info | grep "Docker Root Dir"
```

### Запуск приложения в Docker
1. Скопируйте в папку ts_core:
   - файл docker-compose.production.yml
   - папку system_config
2. Загрузите/обновите образы из Docker Hub:
```
sudo docker compose -f docker-compose.production.yml pull
```
4. Перезапустите сервисы:
```
sudo docker compose -f docker-compose.production.yml down
```
```
sudo docker compose -f docker-compose.production.yml up -d
```
6. Выполните настройки из system_config:
```
cd system_config;
chmod +x setup_socat_proxy.sh;
chmod +x shutdown_counter.sh;
chmod +x update_crontab.sh;
./setup_socat_proxy.sh;
./shutdown_counter.sh;
./update_crontab.sh;
```

### Настройка Nginx
1. Отредактируйте файл /etc/nginx/sites-enabled/default:
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
2. Проверьте и примените конфигурацию:
```
sudo nginx -t
```
```
sudo service nginx reload
```

### ✅ Готово!
Приложение будет доступно по адресу: http://<хост_сервера>/


# monitoring_equipment
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

<!-- Остановка -->
sudo docker compose stop
<!-- Удалить неактивные контейнеры -->
sudo docker container prune -f
<!-- Удалить неиспользуемые образы -->
sudo docker image prune -f

## Автор
<h2 align="center">**Чолий Александр** ([Telegram](https://t.me/alexander_choliy))</h2>
