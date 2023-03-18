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
