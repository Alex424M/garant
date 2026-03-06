from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.property_detail, name='property_detail'),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("application/", views.submit_application, name="submit_application"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('application/delete/<int:pk>/', views.delete_application, name='delete_application'),
]
