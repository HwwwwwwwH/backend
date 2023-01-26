from django.urls import path

from . import views

urlpatterns = [
    path('test', views.index, name='index'),
    path('render/jaw_model', views.get_jaw_model, name='jaw_model'),
]