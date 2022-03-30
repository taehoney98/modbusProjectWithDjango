from django.urls import path
from . import views

urlpatterns = [
    path('',views.index , name='index'),    
    path('coil/<int:index>/',views.writeCoil,name='writeCoil'),
    path('register/<int:register_index>/<int:register_value>', views.writeRegister, name='writeRegister'),
    
]
