""" комманда еженедельной рассылки новых новостей """
import logging
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from news.models import Post, Category

 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу отправке новостей за неделю
def send_messages():
    """ собственно отправка сообщений """
    # выбираем новости за прошедшие 7 дней
    new_posts = Post.objects.filter(
        created__gte=(timezone.now() - timedelta(days=7))
        )
    # проходим по списку пользователей
    for user in User.objects.all():
        if user.email:
            # выбираем новые новости из тех категорий, на которые подписан user
            user_new_post = new_posts.filter(category__in=user.category_set.all())
            if user_new_post:
                # подготовка шаблона и сообщения
                html_content = render_to_string(
                        'news/weekly_posts_mail.html',
                        {'posts': user_new_post, 'count': user_new_post.count(), 'user': user}
                    )
                msg = EmailMultiAlternatives(
                        subject = 'News Paper. Новости за неделю',
                        body=f'Здравствуй, {user.username}. Узнай что произошло за неделю !',
                        from_email = 'shagi80@yandex.ru',
                        to = [user.email,]
                    )
                # привязка HTML и отправка
                msg.attach_alternative(html_content, "text/html")
                msg.send()                
    
 
 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_messages,
            trigger=CronTrigger(
                #second="*/5"
                day_of_week="mon", hour="00", minute="01" 
            ),  
            id="send_weekly_messages",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_messages'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")