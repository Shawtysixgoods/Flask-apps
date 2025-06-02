<!--
Этот обзорный документ описывает используемые модули и библиотеки для создания веб-приложений на Flask.
Он помогает понять, какие технологии могут применяться в проектах.
-->
# Flask-apps

При создании веб-приложений на Flask могут используются следующие модули и библиотеки:

---

## **1. Простые приложения (MVP, лендинги, блоги)**
1. **Минимальный Flask**:  
   `Flask` + `Jinja2` + `Werkzeug`  
2. **Блог без БД**:  
   `Flask` + `Jinja2` + `Markdown` (для статей)  
3. **Блог с SQLite**:  
   `Flask` + `Flask-SQLAlchemy` + `Jinja2`  
4. **Блог с комментариями**:  
   `Flask` + `Flask-SQLAlchemy` + `Flask-WTF` (формы)  
5. **Блог с тегами**:  
   `Flask-SQLAlchemy` + `Jinja2` + `SQLAlchemy` (для many-to-many)  
6. **Блог с пагинацией**:  
   `Flask-SQLAlchemy` + `Flask-Paginate`  
7. **Блог с кэшированием**:  
   `Flask-Caching` (SimpleCache) + `Flask-SQLAlchemy`  
8. **Блог с поиском**:  
   `Flask-WhooshAlchemy` (поиск по статьям)  
9. **Блог с API**:  
   `Flask-RESTful` + `Flask-SQLAlchemy`  
10. **Блог с админкой**:  
    `Flask-Admin` + `Flask-SQLAlchemy`  

### Описание модулей для простых приложений:
- **Flask**: Основной веб-фреймворк, предоставляет базовую функциональность для создания веб-приложений
- **Jinja2**: Шаблонизатор, позволяет создавать HTML-страницы с динамическим контентом
- **Werkzeug**: Набор инструментов для WSGI-приложений, входит в состав Flask
- **Markdown**: Библиотека для работы с Markdown-разметкой, конвертирует текст в HTML
- **Flask-SQLAlchemy**: ORM для работы с базами данных, упрощает взаимодействие с SQLite/PostgreSQL/MySQL
- **Flask-WTF**: Интеграция WTForms с Flask, помогает создавать и валидировать формы
- **Flask-Paginate**: Добавляет пагинацию для разбиения контента на страницы
- **Flask-Caching**: Система кэширования для Flask-приложений
- **Flask-WhooshAlchemy**: Полнотекстовый поиск для Flask-SQLAlchemy (Примечание: устарел, рекомендуется использовать Elasticsearch)
- **Flask-RESTful**: Упрощает создание REST API
- **Flask-Admin**: Автоматически генерирует админ-панель для моделей SQLAlchemy

---

## **2. Аутентификация и пользователи**
11. **Регистрация/логин**:  
    `Flask-Login` + `Flask-WTF` + `Flask-SQLAlchemy`  
12. **Роли и разрешения**:  
    `Flask-Security-Too` + `Flask-SQLAlchemy`  
13. **JWT-аутентификация**:  
    `Flask-JWT-Extended` + `Flask-SQLAlchemy`  
14. **OAuth (Google/GitHub)**:  
    `Authlib` + `Flask-Login`  
15. **Двухфакторная аутентификация**:  
    `Flask-Login` + `Flask-OTP`  
16. **Восстановление пароля**:  
    `Flask-Mail` + `Flask-Security-Too`  
17. **API с токенами**:  
    `Flask-JWT-Extended` + `Flask-RESTful`  
18. **Сессии в Redis**:  
    `Flask-Login` + `Flask-Session` + `redis`  
19. **Анонимные комментарии**:  
    `Flask-WTF` + `Flask-SQLAlchemy`  
20. **Гостевая книга**:  
    `Flask-WTF` + `Flask-SQLAlchemy` + `Jinja2`  

### Описание модулей для аутентификации:
- **Flask-Login**: Управление пользовательскими сессиями и аутентификацией
- **Flask-Security-Too**: Комплексное решение для безопасности (роли, регистрация, сброс пароля)
- **Flask-JWT-Extended**: Работа с JSON Web Tokens для API-аутентификации
- **Authlib**: Реализация OAuth и OpenID Connect протоколов
- **Flask-OTP**: Двухфакторная аутентификация с одноразовыми паролями
- **Flask-Mail**: Отправка email сообщений
- **Flask-Session**: Серверные сессии с поддержкой разных бэкендов
- **redis**: База данных типа ключ-значение, используется для хранения сессий

---

## **3. REST API и микросервисы**
21. **Простое API**:  
    `Flask-RESTful` + `Flask-SQLAlchemy`  
22. **API с JWT**:  
    `Flask-JWT-Extended` + `Flask-RESTful`  
23. **API с документацией**:  
    `Flask-RESTful` + `Flask-Swagger`  
24. **API с кэшированием**:  
    `Flask-Caching` (Redis) + `Flask-RESTful`  
25. **API с GraphQL**:  
    `Graphene-Flask` + `Flask-SQLAlchemy`  
26. **API с CORS**:  
    `Flask-CORS` + `Flask-RESTful`  
27. **API с фоновыми задачами**:  
    `Celery` + `Flask-RESTful`  
28. **API с WebSockets**:  
    `Flask-SocketIO` + `Flask-RESTful`  
29. **API с rate-limiting**:  
    `Flask-Limiter` + `Flask-RESTful`  
30. **API с OAuth2**:  
    `Authlib` + `Flask-RESTful`  

### Описание модулей для REST API:
- **Flask-RESTful**: Создание REST API с поддержкой классов ресурсов
- **Flask-JWT-Extended**: Аутентификация через токены для API
- **Flask-Swagger**: Автоматическая генерация документации API (Примечание: лучше использовать современный flask-openapi3)
- **Flask-CORS**: Поддержка Cross-Origin Resource Sharing
- **Celery**: Асинхронные задачи и очереди
- **Flask-SocketIO**: Реализация WebSocket соединений
- **Flask-Limiter**: Ограничение количества запросов к API
- **Graphene-Flask**: Создание GraphQL API

⚠️ Важные замечания по совместимости:
1. Flask-WhooshAlchemy устарел и не поддерживает новые версии Flask
2. Для поиска рекомендуется использовать Elasticsearch
3. Вместо Flask-Swagger лучше использовать flask-openapi3
4. При использовании Flask-SQLAlchemy важно следить за версиями совместимости с Flask

---

## **4. Базы данных и ORM**
31. **SQLite + SQLAlchemy**:  
    `Flask-SQLAlchemy` + `SQLite`  
32. **PostgreSQL + SQLAlchemy**:  
    `Flask-SQLAlchemy` + `psycopg2`  
33. **MySQL + SQLAlchemy**:  
    `Flask-SQLAlchemy` + `mysqlclient`  
34. **Миграции**:  
    `Flask-Migrate` + `Flask-SQLAlchemy`  
35. **MongoDB (ORM-style)**:  
    `Flask-MongoEngine`  
36. **MongoDB (нативный драйвер)**:  
    `Flask-PyMongo`  
37. **Redis для кэша**:  
    `redis` + `Flask-Caching`  
38. **Elasticsearch**:  
    `Flask-Elasticsearch`  
39. **ClickHouse**:  
    `clickhouse-driver` + `Flask`  
40. **GraphDB (Neo4j)**:  
    `py2neo` + `Flask`  

### Описание модулей для баз данных:
- **Flask-SQLAlchemy**: Python SQL toolkit и ORM
- **psycopg2**: Драйвер PostgreSQL для Python
- **mysqlclient**: Python-MySQL драйвер
- **Flask-Migrate**: Миграции базы данных на основе Alembic
- **Flask-MongoEngine**: MongoDB ORM для Flask
- **Flask-PyMongo**: Нативный драйвер MongoDB
- **redis-py**: Python-клиент для Redis
- **Flask-Elasticsearch**: Интеграция с Elasticsearch
- **clickhouse-driver**: Драйвер для ClickHouse
- **py2neo**: Библиотека для работы с Neo4j

## **5. Веб-сокеты и реальное время**
41. **Чат**:  
    `Flask-SocketIO` + `Flask-Login`  
42. **Уведомления**:  
    `Flask-SocketIO` + `Flask-SQLAlchemy`  
43. **Онлайн-игра**:  
    `Flask-SocketIO` + `redis` (pub/sub)  
44. **Трекер активности**:  
    `Flask-SocketIO` + `Flask-SQLAlchemy`  
45. **Аукцион в реальном времени**:  
    `Flask-SocketIO` + `Flask-Caching`  

### Описание модулей для веб-сокетов:
- **Flask-SocketIO**: WebSocket коммуникация в реальном времени
- **redis**: Pub/Sub для масштабирования WebSocket
- **eventlet**: WSGI-сервер с поддержкой WebSocket
- **gevent**: Альтернативный WSGI-сервер для WebSocket

## **6. Админ-панели и CMS**
46. **Простая админка**:  
    `Flask-Admin` + `Flask-SQLAlchemy`  
47. **Файловый менеджер**:  
    `Flask-Admin` + `Flask-FileUpload`  
48. **Генератор отчетов**:  
    `Flask-Admin` + `Pandas`  
49. **Панель мониторинга**:  
    `Flask-Admin` + `Flask-SQLAlchemy` + `Chart.js`  
50. **Графический редактор**:  
    `Flask-Admin` + `Flask-CKEditor`  

### Описание модулей для админ-панелей:
- **Flask-Admin**: Готовая админ-панель с интерфейсом
- **Flask-FileUpload**: Загрузка и управление файлами
- **Pandas**: Обработка и анализ данных
- **Chart.js**: JavaScript библиотека для визуализации
- **Flask-CKEditor**: Визуальный редактор текста

## **7. Фоновые задачи и очереди**
51. **Отправка email**:  
    `Celery` + `Flask-Mail`  
52. **Парсинг данных**:  
    `Celery` + `BeautifulSoup`  
53. **Генерация PDF**:  
    `Celery` + `ReportLab`  
54. **Обработка видео**:  
    `Celery` + `FFmpeg`  
55. **Web scraping**:  
    `Celery` + `Scrapy`  

### Описание модулей для фоновых задач:
- **Celery**: Распределенная очередь задач
- **BeautifulSoup**: Парсинг HTML и XML
- **ReportLab**: Создание PDF документов
- **FFmpeg-python**: Обработка видео и аудио
- **Scrapy**: Фреймворк для веб-скрапинга

## **8. Оптимизация и масштабирование**
56. **Кэширование страниц**:  
    `Flask-Caching` + `Redis`  
57. **CDN для статики**:  
    `Flask-Static-Compress`  
58. **Асинхронные запросы**:  
    `Flask` + `gevent`  
59. **Балансировка нагрузки**:  
    `Gunicorn` + `Nginx`  
60. **Мониторинг**:  
    `Prometheus` + `Flask-Prometheus`  

### Описание модулей для оптимизации:
- **Redis**: In-memory хранилище данных
- **Flask-Static-Compress**: Сжатие статических файлов
- **gevent**: Асинхронная обработка запросов
- **Gunicorn**: WSGI HTTP сервер
- **Flask-Prometheus**: Метрики для мониторинга

## **9. Интеграции со сторонними сервисами**
61. **Платежи (Stripe)**:  
    `Flask` + `stripe`  
62. **Платежи (PayPal)**:  
    `Flask` + `paypalrestsdk`  
63. **SMS (Twilio)**:  
    `Flask` + `twilio`  
64. **Google API**:  
    `Flask` + `google-api-python-client`  
65. **Telegram Bot**:  
    `Flask` + `python-telegram-bot`  

### Описание модулей для интеграций:
- **stripe**: API для платёжной системы Stripe
- **paypalrestsdk**: SDK для PayPal REST API
- **twilio**: API для SMS и звонков
- **google-api-python-client**: Google API клиент
- **python-telegram-bot**: Telegram Bot API

## **10. Тестирование и CI/CD**
66. **Unit-тесты**:  
    `pytest` + `Flask-Testing`  
67. **Тесты API**:  
    `pytest` + `requests`  
68. **Линтинг**:  
    `Flake8` + `Black`  
69. **CI/CD (GitHub Actions)**:  
    `pytest` + `Docker`  
70. **Логирование**:  
    `Flask` + `Sentry`  

### Описание модулей для тестирования:
- **pytest**: Фреймворк для тестирования
- **Flask-Testing**: Инструменты для тестирования Flask
- **requests**: HTTP-клиент для тестирования API
- **Flake8**: Линтер кода
- **Black**: Форматирование кода
- **Sentry-SDK**: Отслеживание ошибок

## **11. Десктоп и мобильные приложения**
71. **Electron + Flask API**:  
    `Flask-RESTful` + `Electron`  
72. **React Native + Flask**:  
    `Flask-JWT` + `React Native`  
73. **Kivy + Flask**:  
    `Flask` + `Kivy`  
74. **Flutter + Flask**:  
    `Flask-JWT` + `Flutter`  
75. **PyQt + Flask**:  
    `Flask` + `PyQt`  

### Описание модулей для десктоп/мобильных приложений:
- **Electron**: Создание десктоп приложений
- **React Native**: Мобильная разработка
- **Kivy**: Python фреймворк для GUI
- **Flutter**: SDK для мобильной разработки
- **PyQt**: GUI фреймворк для десктоп

## **12. Разное**
76. **Генератор QR-кодов**:  
    `Flask` + `qrcode`  
77. **Погодное приложение**:  
    `Flask` + `OpenWeatherMap API`  
78. **Генератор мемов**:  
    `Flask` + `Pillow`  
79. **Сокращатель ссылок**:  
    `Flask` + `Flask-SQLAlchemy`  
80. **VPN-сервер**:  
    `Flask` + `OpenVPN`  

### Описание модулей для разных задач:
- **qrcode**: Генерация QR-кодов
- **requests**: HTTP запросы к API
- **Pillow**: Обработка изображений
- **SQLAlchemy**: ORM для базы данных
- **OpenVPN**: VPN сервер

⚠️ Дополнительные замечания по совместимости:
1. Для WebSocket убедитесь, что ваш WSGI сервер поддерживает их (например, gunicorn + gevent)
2. При использовании Celery важно правильно настроить брокер сообщений (Redis/RabbitMQ)
3. Для продакшена рекомендуется использовать PostgreSQL вместо SQLite
4. При работе с Flask-SocketIO желательно использовать eventlet или gevent

