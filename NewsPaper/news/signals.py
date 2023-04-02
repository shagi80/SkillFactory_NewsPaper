""" сигналы модуля news """
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category


# сигнал нужно вешать на M2M поле Category, иначе Category недоступно
# сигнал будет срабатывать при первом добавлении новости
# а также при добавлении категории в существующую новость
@receiver(m2m_changed, sender=Post.category.through)
def send_email(sender, instance, **kwargs):
    """ отправка уведомления об создании новости """
    # составляем список адресов
    if kwargs['action'] == "post_add" and kwargs["model"] == Category:
        for category in instance.category.all():
            for user in category.subscribers.all():
                if user.email:
                    # рендеринг HTML шаблона
                    html_content = render_to_string(
                        'news/post_mail.html',
                        {'post': instance, 'category': category, 'user': user}
                    )
                    # подготовка сообщения
                    msg = EmailMultiAlternatives(
                        subject = instance.title,
                        body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!',
                        from_email = 'shagi80@yandex.ru',
                        to = [user.email,]
                    )
                    # привязка HTML и отправка
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
