from django.urls import path, re_path
from index import views

urlpatterns = [
    # path('', views.index),
    path('', views.index),
    path('<int:id>.html', views.models_index),
    path('login.html', views.login),
    # path('<year>/<int:month>/<slug:day>', views.mydate)
    re_path('(?P<year>[0-9]{4}).html', views.mydate, name='myyear'),
    re_path('dict/(?P<year>[0-9]{4}).htm', views.myyear_dict, {'month': '05'}, name='myyear_dict'),
    path('download.html', views.download)
]
