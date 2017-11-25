from django.contrib import admin
from .models import Activity, Action, UserResponse

# Register your models here.
admin.site.register(Activity)
admin.site.register(Action)
admin.site.register(UserResponse)