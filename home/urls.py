from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name='home'

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.SignUp, name='signup'),
    path("login/<pk>/",views.login_user,name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)