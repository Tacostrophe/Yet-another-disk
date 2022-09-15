# Yad


### Описание
**Yet another disk** — проект облачного сервиса, имитирующий систему хранения пользовательских данных.

#### Доступный функционал:
- добавление/обновление файлов/папок (/imports);
- удаление файлов/папок (/delete<id>);
- получение файла по идентификатору (/nodes/<id>);
- получение списка файлов, обновленных в течении суток до указанного времени (/updates).

### Технологии в проекте
- Python 3.7;
- Django 3.2.15;
- Django Rest Framework 3.13.1;
- Docker 20.10.16;
- PostgreSQL;

### Инструкция по развертыванию

Клонировать репозиторий:

```
git clone https://github.com/Tacostrophe/Yet-another-disk.git
```
Перейти в папку enrollment/infra/

Сборка контейнеров:
```
docker compose build
```
Запуск контейнеров:
```
docker compose up -d
```
Выполнить по очереди команды:
```
docker compose exec web python3 manage.py migrate --run-syncdb
```
Теперь проект доступен по адресу http://localhost