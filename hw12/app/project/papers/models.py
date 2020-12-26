from django.db import models

# Create your models here.


class Paper(models.Model):
    source_name = models.CharField('Название ресурса', max_length=200,
                                   null=True)
    author = models.CharField('Имя фамилия автора', max_length=200, null=True)
    title = models.CharField('Заголовок', max_length=200, null=True)
    url = models.URLField("Ссылка на статью", max_length=400, null=True)
    description = models.TextField("Описание статьи", null=True)
    published_at = models.DateField("Дата публикации", null=True)
