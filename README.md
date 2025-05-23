Natalis Domini моё арт-пространство.
реализация проекта по адресу: https://natalis-domini.ru

Создать SPA-приложение на основе Bootstrap.
Создать:
- галерею в виде однополосной карусели с функцией фильтрации объектов по жанрам картин.
- контакты.
- форму запроса обратной связи. Форма запроса обратной связи должна быть подключена к 
телеграм боту для динамического вывода сообщений (не через электронную почту).
Для формы обратно связи создать ограничение: можно было написать с одного почтового ящика до 3х раз.
- небольшое описание рубрики о себе.
админка:
3 модели:
- Жанры
- Серии
- Картины - вывести так же возможность вывода картинки в сущности при чтении всех объектов.

------------------------------------------------------------------------------------------------------------------------

Реализация:
------------------------------------------------------------------------------------------------------------------------
Галерею решил реализовывать методом вывода карточек через JS script. Прикрепил фильтрацию по жанрам к списку объектов.
Работу по отлову новых сообщений решил через фоновую задачу в Celery.
Валидацию для 3х попыток написания сообщений по одному email прописал на уровне формы.
В index.html 2 формы: одна для фильтрации картин, вторая для POST запроса (обратной связи). Вся логика прописана в def
index. В index.html отправляются 3 объекта: список картин (pictures), forms (фильтр картин), post_forms(обратная связь).
------------------------------------------------------------------------------------------------------------------------
Логика полей: название, описание, материал, :
------------------------------------------------------------------------------------------------------------------------
В жанрах и серии - простые названии, а в Картинах должно быть описание. описание складывается из порядкового номера ранее
созданной серии по этой теме. Например, если серия животные, и это первая картина, то поле название будет состоять из 
Серия обезьянки № 1. Описание уже состоит из: название + размер + краска. Соединяет описания все эти сущности.
Логика порядкового номера: берет название серии и ищет отсортированный список сущностей в БД по названию, сортирует и,
выдает последний элемент. Затем просто добавляет к нему значение + 1. Вся логика прописана в переопределенном методе 
save моделей. 
========================================================================================================================
Поля значение, краска, материал берут из модели созданные значения:
size = dict(_40x60='40x60 см', _30x40='30x40 см', _50x60='50x60 см', _20x20='20x20 см')
paint = dict(oil='масляные', acrylic='акриловые', tempera='темпера')
materials = dict(thick_cardboard='плотный картон, хлопок', fiberboard_canvas='холст на ДВП, хлопок',
                 canvas_on_a_stretcher='холст на подрамнике')

Deploy:
Развертывание на сервере
Клонируйте репозиторий на сервер:

Примеры команд:
git clone https://github.com/Iceeyess/art-gallery.git /opt/art-gallery
cd /opt/art-gallery

Создайте файл .env.server в корне проекта и заполните его переменными окружения по модели .env.example.
Запустите Docker Compose:

docker-compose up -d

Настройте SSL-сертификаты с помощью Let's Encrypt:
Убедитесь, что домен natalis-domini.ru указывает на IP-адрес вашего сервера, и выполните следующие команды:

sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d natalis-domini.ru -d www.natalis-domini.ru
После этого Certbot автоматически обновит ваш nginx.conf и настроит SSL.

Перезапустите Nginx:
docker-compose restart nginx
