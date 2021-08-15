# Старый вариант. В новом реализовано с помощью Celery

# import logging
# from datetime import datetime, timezone, timedelta
#
# from django.conf import settings
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
#
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from news.models import Category
#
# logger = logging.getLogger(__name__)
#
#
# def send_to_subscribers():
#     """ Рассылает пользователям список статей из тех категорий, на которые они подписаны, за неделю """
#     categories = Category.objects.all()
#     for category in categories:
#         cat_posts = category.post_set.filter(creation_datetime__gt=datetime.now(timezone.utc) - timedelta(days=7))
#         print(category, cat_posts)
#         if cat_posts:
#             subscribers = category.subscribers.all()
#             for subscriber in subscribers:
#                 print(subscriber)
#                 if subscriber.email:
#                     print('отправка...')
#                     # Отправка HTML
#                     html_content = render_to_string(
#                         'mail_week.html', {
#                             'category': category,
#                             'cat_posts': cat_posts,
#                         }
#                     )
#                     msg = EmailMultiAlternatives(
#                         subject='Список новостей за неделю',
#                         from_email='pozvizdd@yandex.ru',
#                         to=[subscriber.email, 'olegmodenov@gmail.com'],
#                     )
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.send()
#
#
# # функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             send_to_subscribers,
#             # trigger=CronTrigger(second="*/10"),
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
