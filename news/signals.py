# Старый вариант, реализовано с помощью Celery

# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
#
# from .models import Post
#
#
# # Отправляет по почте информацию о том, что добавлен новый пост в категории, на которую подписан пользователь
# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers(sender, instance, **kwargs):
#     action = kwargs['action']
#     if action == 'post_add':
#         categories = instance.category.all()
#         for category in categories:
#             subscribers = category.subscribers.all()
#             for subscriber in subscribers:
#                 if subscriber.email:
#                     # Отправка HTML
#                     html_content = render_to_string(
#                         'mail.html', {
#                             'user': subscriber,
#                             'text': f'{instance.text[:50]}',
#                             'post': instance,
#                         }
#                     )
#                     msg = EmailMultiAlternatives(
#                         subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!',
#                         from_email='pozvizdd@yandex.ru',
#                         to=[subscriber.email, 'olegmodenov@gmail.com'],
#                     )
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.send()
#
#                     # # Отправка простого текста
#                     # send_mail(
#                     #     subject=f'{subscriber.email}',
#                     #     message=f'Появился новый пост!\n {instance.title}: {instance.text[:50]}.',
#                     #     from_email='pozvizdd@yandex.ru',
#                     #     recipient_list=[subscriber.email, 'olegmodenov@gmail.com'],
#                     # )
