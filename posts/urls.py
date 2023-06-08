from django.urls import path

from .views import *

urlpatterns = [
    path('search/', search, name='search'),
    path('<slug:category_slug>/<slug:slug>/', detail, name='post_detail'),
    path('<slug:slug>/', category, name='category_detail'),
    path('dash/base/show/', dash_base, name='dash_base'),
    path('category/add_category', add_category , name='add_category'),
    path('category/edit_category/<slug:slug>/', edit_category , name='edit_category'),
    path('category/update_category/<slug:slug>/', update_category , name='update_category'),
    path('category/delete_category/<slug:slug>/', delete_category , name='delete_category'),
    path('post/add_post', add_post , name='add_post'),
    path('post/edit_post/<slug:slug>/', edit_post , name='edit_post'),
    path('post/update_post/<slug:slug>/', update_post , name='update_post'),
    path('post/delete_post/<slug:slug>/', delete_post , name='delete_post'),
    path('like/<slug:category_slug>/<slug:slug>/',like,name='like')
]
