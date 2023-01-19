from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Menu, Cart, Order, Category
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .serializers import MenuSerializers,CategorySerializers, UserSerializers, CartSerializers
from . import serializers
from .permissions import IsManager
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage
from datetime import date
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import get_user_model
import json

# Create your models here.
User = get_user_model()
# Create your views here.


class MenuListView(generics.GenericAPIView):

    serializer_class = serializers.MenuSerializers
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        category = request.query_params.get('category')
        price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=3)
        page = request.query_params.get('page', default=1)
        menus = Menu.objects.all()
        if category:
            menus = menus.filter(category__title=category_name)
        if price:
            menus = menus.filter(price__lte=price)
        if search:
            menus = menus.filter(title__icontains=search)
        if ordering:
            ordering = ordering.split(",")
            menus = menus.order_by(*ordering)
        paginator = Paginator(menus, per_page=perpage)
        try:
            menus = paginator.page(number=page)
        except EmptyPage:
            menus = []
        menus = self.serializer_class(menus, many=True)
        return Response(data = menus.data, status = status.HTTP_200_OK)
    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class MenuSingleView(generics.GenericAPIView):
    serializer_class = serializers.MenuSerializers
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        menu = get_object_or_404(Menu, id=pk)
        serializer = self.serializer_class(menu)
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk):
        if not request.user.is_staff:
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        menu = get_object_or_404(Menu, pk = pk)
        serializer = self.serializer_class(data=data, instance=menu)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        if not request.user.is_staff:
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        menu = get_object_or_404(Menu, pk = pk)
        serializer = self.serializer_class(data=data, instance=menu, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        menu = get_object_or_404(Menu, pk = pk)
        menu.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class CategoryListView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializers
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorySingleView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializers
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        category = get_object_or_404(Category, pk = pk)
        serializer = self.serializer_class(category)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    def patch(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        category = get_object_or_404(Category, pk = pk)
        serializer = self.serializer_class(data=data,instance=category, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    def delete(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        category = get_object_or_404(Category, pk = pk)
        category.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


class ManagerListView(generics.GenericAPIView):
    serializer_class = serializers.MenuSerializers
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = Order.objects.all()
        managers = User.objects.filter(groups__name="Manager").all()
        serialized = UserSerializers(managers, many=True)
        return Response(serialized.data)
    def post(self, request):
        queryset = Order.objects.all()
        user = request.data["username"]
        user = get_object_or_404(User, username = user)
        manager = Group.objects.get(name="Manager")
        manager.user_set.add(user)
        data = {"message": "User {} added successfully to the manager group".format(user)}
        return Response(data = data, status=status.HTTP_201_CREATED)


class GroupListCreate(generics.GenericAPIView):
    serializer_class = serializers.GroupSerializers
    permission_classes = [IsAdminUser]
    def get(self, request):
        group_name = request.GET.get('group_name')
        username = request.GET.get('username')
        activity = request.GET.get('activity')
        if group_name and username:
            group = get_object_or_404(Group, name=group_name)
            user = get_object_or_404(User, username=username)
            if activity == "add":
                user.groups.add(group)
                return Response(data = {"message": "User {} added to group {}".format(username, group_name)}, status = status.HTTP_200_OK)
            elif activity == "remove":
                user.groups.remove(group)
                return Response(data = {"message": "User {} removed from group {}".format(username, group_name)}, status = status.HTTP_200_OK)
        queryset = Group.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GroupSingle(generics.GenericAPIView):
    serializer_class = serializers.GroupSerializers
    permission_classes = [IsAuthenticated, IsManager]
    def get(self, request, pk):
        group = get_object_or_404(Group, pk = pk)
        serializer = self.serializer_class(group)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        group = get_object_or_404(Group, pk = pk)
        serializer = self.serializer_class(data=data,instance=group, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    def delete(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        group = get_object_or_404(Group, pk = pk)
        group.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


class CartMenu(generics.GenericAPIView):
    serializer_class = serializers.CartSerializers
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_cart = get_object_or_404(Cart, user = request.user)
        serialized = self.serializer_class(user_cart, many=True)
        return Response(serialized.data)
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.GenericAPIView):
    serializer_class = serializers.CartSerializers
    permission_classes = [IsAuthenticated]