from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Menu, Cart, Order, OrderItem
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .serializers import MenuItemsSerializers, UserSerializers, CartSerializers, OrderSerializers, OrderItemsSerializers
from .permissions import IsManager
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from datetime import date
from rest_framework.throttling import UserRateThrottle
# Create your views here.


class MenuListView(generics.GenericAPIView):

    serializer_class = serializers.MenuItemsSerializers
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    category = request.query_params.get('category')
    price = request.query_params.get('to_price')
    search = request.query_params.get('search')
    ordering = request.query_params.get('ordering')
    perpage = request.query_params.get('perpage', default=3)
    page = request.query_params.get('page', default=1)
    def get(self, request):
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

    def delete(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            data = {'message': '403 - Unauthorized, Access Denied'}
            return Response(data = data, status=status.HTTP_403_FORBIDDEN)
        menu = get_object_or_404(Menu, pk = pk)
        menu.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class CategoryListView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializers
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(queryset, many=True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)


class CategorySingleView(generics.GenericAPIView):
    serializer_class = serializers.CategorySerializers
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    def  post(self, request, pk):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ManagerListView(generics.GenericAPIView):
    serializer_class = serializers.MenuItemsSerializers
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        managers = User.objects.filter(groups__name="Manager").all()
        serialized = UserSerializers(managers, many=True)
        return Response(serialized.data)
    def post(self, request):
        user = request.data["username"]
        user = get_object_or_404(User, username = user)
        manager = Group.objects.get(name="Manager")
        manager.user_set.add(user)
        data = {"message": "User {} added successfully to the manager group".format(user)}
        return Response(data = data, status=status.HTTP_201_CREATED)


class GroupListCreate(generic.GenericAPIView):
    serializer_class = serializers.GroupSerializers
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = self.serializer_class(queryset, many=True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)


class GroupListCreate(generic.GenericAPIView):
    serializer_class = serializers.GroupSerializers
    permission_classes = [IsAuthenticated, IsManager]
    def  post(self, request, pk):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     data = request.data
    #     new_group = Group.objects.get_or_create(name ='new_group')


class CartMenu(generic.GenericAPIView):
    serializer_class = serializers.CartSerializers
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pass
    def  post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


