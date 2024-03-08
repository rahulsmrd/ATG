from django.contrib import admin
from django.urls import path, include
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('',index.as_view() ,name="home"),
    path('detail/<pk>/',detail_post.as_view() ,name="detail"),
    path('create/',create_post.as_view() ,name="create"),
    path('update/<pk>/',update_post.as_view() ,name="update"),
    path('delete/<pk>/',delete_post.as_view() ,name="delete"),
    path('publish/<pk>/',publish,name="publish"),
]