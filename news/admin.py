from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    # отобразить в админке
    list_display = ('id', 'title', 'creation_datetime')
    list_display_links = ('id', 'title')  # Ссылки на новость в админке

    search_fields = ('title', 'text')  # Поля для поиска
    list_filter = ('rating', 'type', 'category__title')  # Фильтр


admin.site.register(Post, PostAdmin)
admin.site.register(Category)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
