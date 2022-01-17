from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        if self.parent is None:
            super(Category, self).save(*args, **kwargs)
        elif self.parent.level == 3:
            raise ValueError(u'Достигнута максимальная вложенность!')
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание')
    scope = models.CharField(max_length=50, verbose_name='Сфера применения')
    diameter = models.FloatField(verbose_name='Диаметр')
    length = models.IntegerField(verbose_name='Длина')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    picture = models.ImageField(upload_to='static/pictures', verbose_name='Изображение')
    card = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.card.level != 3:
            raise ValueError(u'Нельзя привязать продукт не к карточке!')
        super(Product, self).save(*args, **kwargs)
