from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('newsub', views.newsub),
    path('remove/<int:id>', views.delete),
    path('edit/<int:id>', views.edit),
    path('changecurrency', views.change_currency),
    path('editprofile', views.edit_profile),
    path('changepw', views.change_password),
    path('market', views.market_view_preferred),
    path('report/<str:email>/<str:m>', views.report_scammer),
    path('marketall', views.market_all)
]