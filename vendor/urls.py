from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('orders/', views.orders , name= 'orders'),
    path('earnings', views.earnings , name= 'earnings'),
    path('statement', views.statement , name= 'statement'),
    path('changepassword/', views.changepassword , name= 'changepassword'),
    path('logout/', AccountViews.logout , name= 'logout'),
    # Category CRUD
    path('menu-builder/', views.menu_builder, name= 'menu_builder'),
    path('menu-builder/category/<int:pk>/', views.foodItem_by_category, name='foodItem_by_category'),
    path('menu-builder/category/add', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),
    # Food Item CRUD
    path('menu-builder/category/editItem/<int:pk>', views.edit_foodItem, name='edit_foodItem'),
    path('menu-builder/category/deleteItem/<int:pk>', views.delete_foodItem, name='delete_foodItem'),
]