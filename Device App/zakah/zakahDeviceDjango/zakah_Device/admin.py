from django.contrib import admin
from . models import Organizations,Types,Sub_types,Transaction

# Register your models here.
admin.site.register(Organizations)
admin.site.register(Types)
admin.site.register(Sub_types)
admin.site.register(Transaction)