from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.MenuListView.as_view(), name= "menu_list"),
    path('menu-items/<int:pk>', views.MenuSingleView.as_view(), name = "single_menu"),
    path('groups/manager/users', views.ManagerListView.as_view(), name="managers"),
    path('categories', views.CategoryListView.as_view(), name= "categories"),
    path('cart/menu-items', views.CartMenu.as_view(), name="cart-menu"),

    # path('groups/manager/users/<int:pk>', views.delManager),

]
