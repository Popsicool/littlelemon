from rest_framework import serializers
from .models import Menu, Category, Cart, Order
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class MenuSerializers(serializers.ModelSerializer):
    # category = CategorySerializers(read_only=True)
    # category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Menu
        fields = ['title', 'price',
                  'featured', 'category']

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class UserSerializers(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField(method_name="group_name")

    class Meta:
        model = User
        fields = ["id", 'username', 'email', 'groups']

    def group_name(self, person: User):
        return [x.name for x in person.groups.all()]


class CartSerializers(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name="totalprice")
    menuitem = MenuSerializers(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "menuitem", "menuitem_id",
                  "quantity", "unit_price", "price"]

    def totalprice(self, model: Cart):
        return model.price * model.quantity

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]
