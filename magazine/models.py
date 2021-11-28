from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    online_wallet = models.DecimalField(decimal_places=2, max_digits=12, default=1000.00)


class Product(models.Model):
    product_name = models.CharField(max_length=120)
    product_description = models.TextField(max_length=10000, null=True)
    product_price = models.PositiveIntegerField()
    product_count = models.PositiveIntegerField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.product_name


class ObjectBuyProduct(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='user')
    product_name = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='object_product_name')
    number_of_product = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return f'{self.user}', {self.product_name}, {self.created_at}


class PurchaseReturn(models.Model):
    return_at = models.DateTimeField(auto_now_add=True)
    proof_of_return = models.BooleanField(default=False)
    object_buy_product = models.OneToOneField(ObjectBuyProduct, on_delete=models.DO_NOTHING, related_name='purchase_return')

    class Meta:
        ordering = ['-return_at', ]

