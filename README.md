Короче
Если у вас есть Postgres на компе, то с кайфом, вы сможете развернуть проект
Как это делать:
В терминале в папке проекта:
psql -U postgres
Далее нужно будет ввести свой пароль от Postgres(Он где-то у вас локально хранится)
Далее вводим:
CREATE USER virtual_dean_user WITH PASSWORD '11727';
ALTER USER virtual_dean_user CREATEDB;
CREATE DATABASE virtual_dean_db OWNER virtual_dean_user;
ALTER DATABASE virtual_dean_db OWNER TO virtual_dean_user;
GRANT ALL PRIVILEGES ON DATABASE virtual_dean_db TO virtual_dean_user;

\c virtual_dean_db

GRANT ALL ON SCHEMA public TO virtual_dean_user;
\q

Теперь инициализируем БД:
psql -U virtual_dean_user -d virtual_dean_db -f init_virtual_dean.sql
Пароль: 11727

Потом активируем виртуальное окружение
.\venv\Scripts\Activate.ps1
Запускаем 
python main.py