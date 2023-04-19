# Module_D_NewsPaper

Module D2.7 Получение данных из моделей

Предположил, что модель Author должна описываться в созданном ранее на одном из практических заданий
приложении Accounts. Туда и положил

Файл с коммандами консоли в папке 'NewsPaper'


Module D4.2. GET-параметры в действии.

Добавлен пагинатор. Для удобства использования на разных страницах пагинатор вынесен в include-шаблон

Добавлен django-filters. Для универсалиазации отображения заголовков новостей на странице общего списка
и на странице поиска html-код описывающий вывод заголовка вынесен в inclusion-тэг

Для сохранения параметров фильтрации при использвоании пагинатора в код пагинатора добавлен тэг,
копирующий и подставляющий параметры фильтра из строки запроса.


Module D4.4. Продолжаем дружить с формами. Редактируем уже записанную информацию. Удаляем ненужные объекты.

При реализации функций добавления новости пришлось решать проблему аунтефикации пользователя. Модель Post
имеет обязательное поле Author и значит пользователь, пытающийся создать объект, должне быть авторизован
на сайте и быть автором. Использованы LoginRequiredMixin  и UserPassesTestMixin хотя
опять же все это работает криво - только если юзеры административный персонал сайта (что бы в виду отсутствия
формы авторизации на самом сайте можно было авторизоваться через админку)

user1 - K3s4yrk1
user2 - K3s4yrk2

При создании и изменении новости поле "автор" заполняется не явно.

Редактирование и удаление новости разрешено только автору этой новости и суперпользователю.

Кнопки "Изменить" и "Удалить" на странице новости+


Module D5.4. Возможности регистрации в Django.

Добавлен вход и выход через allauth. Вход по e-mail и аккаунту Google
Минимальная стилизация базового шаблона.
Добавлена кнопка "войти/выйти" на панель навигации
Определны переменные LOGIN_URL, LOGOUT_REDIRECT_URL

Вход либо по кнопке "войти" на панели навигации, либо при попрытке Добавить нвоость:
user1 - shagi80@mail.ru - K3s4yrk1

Авторизованные пользователи не являющиеся авторами новость добавлять не могут.


Module D5.5. Группы пользователей

Форма входа allauth расширена неявным добавленем в групуу пользователей. Форма в Newspaper.accounts.form
На панель навигации добавлена кнопка "стать автором". Скрытие/показ кнопки авторам/не авторам настроены.
Фнукция добавления в группу в Newspaper.accounte.view. Одновременно с добавлением в группу создается
соовтетствующий обьект Author


Module D5.6. Права доступа

Установленны права группам пользователя. Доступ к предсталениям управляется через PermissionRequiredMixin


Module D6.2. Отправляем письма через Django

На старнице новостей добавлена возможность выбора категории. При выборе категории доступна кнопка "Подписаться"
Зарегистрированный пользователь подписывается на категорию.
Добавлена процедура отправки сообщения по электронной почте после создания новой новости.


Module D6.3. Django-allauth и email

Подтверждение регистрации по электронной почте через allauth


Module D6.4. Отправка электронных писем по событию, знакомство с сигналами

Добавлен сигнал на добавление M2M поля Post.category
Ограничение возможности добавления более чем 3х новостей за 24 часа реализовано в методе dispatch представления CreatePost


Module D6.5. Периодические задачи

Добавлена переодическая задача - рассылка новых писем в конце недели


Module D7.3. Кэширование в Django

Кэширован вывод новости на странице новости по 5 мин
На странице списка новостей отдельно кэшировано меню выбора категории на 10 мин и остальное содержимое на 1 мин.
"Главная" страница - кэширована.
Кэширована не изменяющаяся часть navbar


Module D7.4. Кэширование на низком уровне

Добавлено кэширование объекта новости в представлении
испрвлены ошбки в кэшировании шаблонов


Module D10.4. Написание собственных команд

Добавлена команда удаления новостей из определенной категории
deletemews <категория>




Разобрался как не отправлять на GitHub *.djcache файлы