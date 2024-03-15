from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name='home'

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.SignUp, name='signup'),
    path("login/<pk>/",views.login_user,name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("change_password/",views.PasswordChangeView.as_view(),name="change_password"),
    path('update_profile/<pk>/',views.update_profile_data.as_view(),name="update_profile"),
    path('book/',views.book_appointment.as_view(),name="book_appointment"),
    path('book_appointment/<pk>/',views.appointment,name="appointment"),
    path('confirm/<pk>/',views.confirmation,name="confirmation"),
    path('appointment_details/<pk>/',views.appointment_details.as_view(),name="appointment_details"),
    path('dele_confirm/<pk>/',views.dele_confirm,name="dele_confirm"),
    path('delete_appointment/<pk>/',views.delete_appointment,name="delete_appointment"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)