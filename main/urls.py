from django.urls import path

from . import views

urlpatterns = [
    path('test', views.index, name='index'),
    path('case_existence', views.get_case_existence, name='case_existence'),
    path('render/raw_files_info', views.get_raw_files_info, name='files_info'),
    path('render/dicom_files', views.get_dicom_files, name='dicom_files'),
    path('render/jaw_model', views.get_jaw_model, name='jaw_model'),
    path('render/teeth_list', views.get_teeth_list, name='teeth_list'),
    path('render/tooth_model', views.get_tooth_model, name='tooth_model'),
    path('render/upload/jaw', views.upload_jaw_model, name='upload_jaw'),
]