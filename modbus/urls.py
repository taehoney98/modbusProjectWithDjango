from django.urls import path
from . import views
from modbus.views import AnalogRestAPI, DigitalRestAPI

urlpatterns = [
    path('',views.index , name='index'),    
    path('coil/<int:index>/',views.writeCoil,name='writeCoil'),
    path('register/<int:register_index>/<int:register_value>', views.writeRegister, name='writeRegister'),
    path('test/', DigitalRestAPI.as_view()),
    path('test/<int:id>',DigitalRestAPI.as_view()) ,
    path('analogapi/',AnalogRestAPI.as_view()),
    path('analogapi/<int:id>',AnalogRestAPI.as_view()),
]
