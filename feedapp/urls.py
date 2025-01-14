from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("policy", views.policy, name="policy"),
    path("<int:pk>/", views.detail, name="detail"),
    path("terms", views.terms, name="terms"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
]
