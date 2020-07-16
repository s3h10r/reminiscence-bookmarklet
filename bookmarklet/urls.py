from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='show'),
    path('get/', views.get, name='get'),
    # TODO
    path('add-url/', views.add_to_reminiscence, name='add_url'),
]
