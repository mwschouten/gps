from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Delivery)
admin.site.register(Project)
admin.site.register(Series)
admin.site.register(History)

class MAdmin(admin.ModelAdmin):
    list_display = ('timestamp','partof','value','val_min','val_max',)

class LocAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'lon','lat', 'last_upload']

    def last_upload(self, obj):
        ll = obj.series_set.all().latest('id')
        if ll:
            return str(ll)
        else:
            return '-'
   
admin.site.register(Measurement,MAdmin)
admin.site.register(Location,LocAdmin)
