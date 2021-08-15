from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все посты определенной категории'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Выберете категорию, есть категории:')
        for category in Category.objects.all():
            self.stdout.write(f'{category}')

        answer_category = input()
        for category in Category.objects.all():
            if category.title == answer_category:
                self.stdout.write('Вы действительно хотите удалить посты в категории? yes/no')
                answer = input()  # считываем подтверждение

                if answer == 'yes':
                    category.post_set.all().delete()
                    self.stdout.write(self.style.SUCCESS(f'Посты в категории {answer_category} удалены!'))
                    return
                else:
                    self.stdout.write(self.style.ERROR('Не подтверждено, посты не удалены'))
                    return

            else:
                self.stdout.write('Такой категории нет')
                return
