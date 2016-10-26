from django.contrib import admin
from .models import User
from .models import Note


admin.site.register(User)
admin.site.register(Note)
