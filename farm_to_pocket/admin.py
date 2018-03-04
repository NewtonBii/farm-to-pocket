from django.contrib import admin
from .models import User,Product,session_levels

admin.site.register(User)
admin.site.register(Product)
admin.site.register(session_levels)