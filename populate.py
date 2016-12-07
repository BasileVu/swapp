import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swapp.settings")

import django
django.setup()

from users.models import *
from items.models import *

def create_item(category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, 
								   price_max=price_max, archived=archived, category=category, owner=owner)

if __name__ == '__main__':    
	u1 = User.objects.create_user(username="user1", email="test@test.com", password="password")
	u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password")

	c1 = Category.objects.create(name="Test")
	c2 = Category.objects.create(name="Test2")
	c3 = Category.objects.create(name="Test3")

	create_item(c1, u1, name="Shoes", description="My old shoes", price_min=10, price_max=30)
	create_item(c2, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30)
	create_item(c3, u1, name="Ring", description="My precious", price_min=100, price_max=500)
	create_item(c1, u2, name="New mouse", description="Brand new", price_min=20, price_max=100)
	create_item(c2, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000)

