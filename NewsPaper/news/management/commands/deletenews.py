""" команда удаления новостей из определенной категории """
from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post
 
class Command(BaseCommand):
    """ команда удаления новостей из определенной категории """
    help = 'Удаление новостей из определенной категории' # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Категория не указана !'
    requires_migrations_checks = True # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)
 
    def add_arguments(self, parser):
        # добавляем аргумент
        parser.add_argument('category', type=str)
 
    def handle(self, *args, **options):
        # запрашиваем подтверждение
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no - ')
        
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(title__iregex=options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Удаление новостей из категории "{category.title}" произошло успешно !')) # в случае неправильного подтверждения говорим, что в доступе отказано
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория  "{options["category"]}" не найдена !'))