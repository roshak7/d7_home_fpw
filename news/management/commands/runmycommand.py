from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Выводит числа-аргументы'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполняется при вызове вашей команды
        self.stdout.write(str(options['argument']))