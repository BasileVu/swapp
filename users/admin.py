from django.contrib import admin
from .models import UserProfile
from .models import Note


admin.site.register(UserProfile)
admin.site.register(Note)
