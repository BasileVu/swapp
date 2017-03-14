from django.contrib import admin
from .models import Item
from .models import Image
from .models import Category
from .models import Like


admin.site.register(Item)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Like)
