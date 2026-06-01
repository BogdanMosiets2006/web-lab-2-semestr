    WORKLOAD-APP — Учебная нагрузка преподавателя
    Laravel 12 + Vue.js 3 + Bootstrap 4 + Filament Admin

ТРЕБОВАНИЯ:
- PHP 8.2+ (расширения: intl, mbstring, pdo_mysql, zip)
- Composer
- Node.js 18+ / npm
- MySQL 5.7+ / MariaDB 10.4+

УСТАНОВКА:

1. Распаковать архив в папку проекта

2. Установить зависимости:
   composer install
   npm install

3. Настроить окружение:
   copy .env.example .env

   Открыть .env и настроить базу данных:
   DB_DATABASE=workload_db
   DB_USERNAME=root
   DB_PASSWORD=

4. Создать базу данных в MySQL:
   CREATE DATABASE workload_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

5. Сгенерировать ключ:
   php artisan key:generate

6. Запустить миграции:
   php artisan migrate

7. (Опционально) Заполнить тестовыми данными:
   php artisan workload:fill --count=30

8. Собрать фронтенд:
   npm run build

9. Запустить сервер:
   php artisan serve

10. Открыть в браузере:
    http://localhost:8000

ИСПОЛЬЗОВАНИЕ:

- Регистрация: http://localhost:8000/register
- Вход: http://localhost:8000/login
- Таблица нагрузки: http://localhost:8000/workload
- Админ-панель (Filament): http://localhost:8000/admin

Функции:
- CRUD (добавление, редактирование, удаление записей)
- Фильтры по семестру и финансированию
- Импорт данных из Excel (.xlsx, .xls)
- Очистка всех записей
- Пагинация и ленивая подгрузка
- Админ-панель Filament

СТРУКТУРА БАЗЫ ДАННЫХ (6 таблиц):

- teachers         (преподаватели)
- departments      (кафедры)
- academic_years   (учебные годы)
- disciplines      (дисциплины)
- workload_records (записи нагрузки — главная таблица)
- uploaded_files   (загруженные файлы)

