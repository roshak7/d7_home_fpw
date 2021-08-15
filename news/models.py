from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"

    def update_rating(self):
        """ суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора."""

        articles = Post.objects.filter(author__user_id=self.user_id)
        articles_rating = 0
        for article in articles:
            articles_rating += article.rating

        author_comments = Comment.objects.filter(user__id=self.user_id)
        author_comments_rating = 0
        for comment in author_comments:
            author_comments_rating += comment.rating

        articles_comments = Comment.objects.filter(post__author__user_id=self.user_id)
        articles_comments_rating = 0
        for comment in articles_comments:
            articles_comments_rating += comment.rating

        self.rating = articles_rating * 3 + author_comments_rating + articles_comments_rating
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('news_category', kwargs={'category_id': self.pk})


class Post(models.Model):
    TYPE = [
        ('Article', 'Статья'),
        ('News', 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField(Category, through='PostCategory')

    type = models.CharField(max_length=20, choices=TYPE, verbose_name='Тип поста', default='Article')
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-creation_datetime', 'title']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('news_one', kwargs={'pk': self.pk})

    # Для кэширования отдельной новости
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:125]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"text: {self.text} and rating: {self.rating}"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
