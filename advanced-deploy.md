## Переменные окружения

* `BOT_CREDENTIALS`: Учётные данные бота. Состоят из блоков
  `cts_host@secret_key@bot_id`, разделённых запятыми (один бот может быть
  зарегистрирован на нескольких CTS). `cts_host` -- адрес админки, `secret_key` и
  `bot_id` можно получить после регистрации бота, нажав на его имя. Инструкция по
  регистрации бота находится в [Руководстве
  администратора](https://express.ms/admin_guide.pdf) `->` Эксплуатация корпоративного
  сервера `->` Управление контактами `->` Чат-боты.
* `POSTGRERS_DSN`: DSN для БД PostgreSQL, например:
  `postgres://postgres_user:postgres_password@postgres:port/db_name`
* `REDIS_DSN`: DSN для хранилища Redis, например: `redis://redis:6379/0`
* `DEBUG` [`false`]: Включает вывод сообщений уровня `DEBUG` (по-умолчанию выводятся
    сообщения с уровня `INFO`).
* `SQL_DEBUG` [`false`]: Включает вывод запросов к БД PostgreSQL.


## Продвинутая инструкция по развертыванию bot-fix

**Примечание**: Чтобы легко добавлять новых ботов на сервер, хранилища находятся в
отдельной docker-сети и используются несколькими ботами сразу (каждый обращается к своей
БД, но к единственному экземпляру PosgreSQL/Redis). При необходимости хранилища и бота
легко объединить в один docker-compose файл.


### Настройка хранилищ, используемых ботом

1. Создайте директорию для PosgreSQL+Redis.

```shell
mkdir -p /opt/express/bots/storages
```

2. В директории `/opt/express/bots/storages` создайте файл `docker-compose.yml` со
   следующим содержимым:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:13.2-alpine
    env_file: .env
    ports:
      - "5432:5432"
    restart: always
    networks:
      - express_bots_storages
    volumes:
      - /opt/express/bots/storages/postgresdata:/var/lib/postgresql/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "10"

  redis:
    image: redis:6.2-alpine
    env_file: .env
    ports:
      - "6379:6379"
    restart: always
    networks:
      - express_bots_storages
    volumes:
      - /opt/express/bots/storages/redisdata:/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "10"

networks:
  express_bots_storages:
    name: express_bots_storages
```

3. Заполните файл `.env` необходимыми данными (для генерации паролей используйте команду
   `openssl rand -hex 16`):

```bash
POSTGRES_USER="postgres"  # Общий пользователь PostgreSQL, у бота будет свой собственный
POSTGRES_PASSWORD="<GENERATE>"
```

4. Запустите контейнеры командой `docker-compose up -d`.
   

5. Убедитесь, что в логах хранилищ нет ошибок.

```bash
docker-compose logs
```


### Настройка бота

1. Создайте БД и пользователя для бота (для генерации паролей используйте команду
   `openssl rand -hex 16`):

```shell
docker exec -it storages_postgres_1 psql --user postgres
```

```sql
CREATE USER bot_fix_user PASSWORD '<GENERATE>';
CREATE DATABASE bot_fix_db;
GRANT ALL PRIVILEGES ON DATABASE bot_fix_db 
  TO bot_fix_user;
```

2. Скачайте репозиторий на сервер:

```bash
git clone <THIS_REPOSITORY> /opt/express/bots/bot-fix
cd /opt/express/bots/bot-fix
```

3. Соберите образ:

```bash
docker build -t bot-fix .
```

При необходимости можно добавить
[дополнительные параметры](https://www.uvicorn.org/#command-line-options). Например:

```bash
docker build -t bot-fix 
  --build-args UVICORN_CMD_ARGS="--ssl-ca-certs TEXT" .
```

4. В директории `/opt/express/bots/bot-fix` создайте файл
   `docker-compose.deploy.yml` со следующим содержимым:

```yaml
version: "3.8"

services:
  bot-fix:
    image: bot-fix
    container_name: bot-fix
    env_file: .env
    ports:
      - "8000:8000"  # Отредактируйте порт хоста (первый), если он уже занят
    restart: always
    depends_on:
      - postgres
      - redis
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "10"

networks:
  default:
    external:
      name: express_bots_storages
```
   
5. Создайте бота в панели администратора eXpress. Хост CTS (в строке браузера, когда вы в админке) и
   "Secret key" пригодятся для заполнения переменной окружения `BOT_CREDENTIALS`. 
   Заполните `.env` необходимыми данными:

```bash
BOT_CREDENTIALS="example.cts.domain@d87f0dce2280d04b41f08e3adb1ae81c@5ce31515-32ae-435a-b6f4-748d2ced921d"
# etc.
```

Описание переменных и примеры можно посмотреть в [соответствующем
разделе](#переменные-окружения).

6. Запустите бота командой:

```bash
docker-compose up -d
```

7. Найдите бота через поиск корпоративных контактов (иконка человечка слева-сверху в
   мессенджере), напишите ему что-нибудь для проверки.


8. Убедитесь, что в логах бота нет ошибок.

```bash
docker-compose logs
```
