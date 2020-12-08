from django.db import models
from datetime import date
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name = 'Имя категории')
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, 
        blank=True, related_name='children'
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent}-->{self.title}-->{self.id}"
        return f"{self.title} --> {self.id}"



class Product(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name = 'Категория', on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=155, verbose_name = 'Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Цена')
    description = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.title



class Choosen(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} --> {self.user}'

# class Orders(models.Model):
#     date = models.DateTimeField(auto_now_add=True)
#     price = models.FloatField(null=True, blank=True)
#     quantity = models.PositiveSmallIntegerField(default=0)

#     def __str__(self):
#         return f"{self.client_id} - {self.seller_id}"


