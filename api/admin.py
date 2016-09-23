from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Delivery)
admin.site.register(Location)
admin.site.register(Project)
admin.site.register(Series)
admin.site.register(History)

class MAdmin(admin.ModelAdmin):
    list_display = ('timestamp','partof','value','val_min','val_max',)

admin.site.register(Measurement,MAdmin)
