from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


# new_group, created = Group.objects.get_or_create(name ='new_group')

class Category(models.Model):
    title = models.CharField(max_length=250)


class Menu(models.Model):
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default= False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    # price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"<Cart {self.id} owned by {self.user.id}>"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="delivery_crew")
    delivered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


# class OrderItem(models.Model):
#     order = models.ForeignKey(User, on_delete=models.CASCADE)
#     menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.SmallIntegerField()
#     unit_price = models.DecimalField(decimal_places=2, max_digits=6)
#     price = models.DecimalField(max_digits=6, decimal_places=2)

#     class Meta:
#         unique_together = ('order', 'menuitem')
