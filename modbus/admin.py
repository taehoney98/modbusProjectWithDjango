from multiprocessing.spawn import old_main_modules
from django.contrib import admin
from .models import Digital, Analog
# Register your models here.

admin.site.register(Digital)
admin.site.register(Analog)
