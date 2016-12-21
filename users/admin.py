from django.contrib import admin
from .models import UserProfile, Consultation
from .models import Note


admin.site.register(UserProfile)
admin.site.register(Note)
admin.site.register(Consultation)
