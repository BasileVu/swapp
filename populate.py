import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swapp.settings")

import django
from PIL import Image as ImagePil

django.setup()

from users.models import *
from items.models import *
from comments.models import Comment
from notifications.models import Notification


def create_item(category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
    return Item.objects.create(name=name, description=description, price_min=price_min,
                               price_max=price_max, archived=archived, category=category, owner=owner)


def create_offer(item_given, item_received, comment="Offer test"):
    return Offer.objects.create(item_given=item_given, item_received=item_received, comment=comment)


def create_comment(user, item, content="Comment test"):
    return Comment.objects.create(content=content, user=user, item=item)


if __name__ == '__main__':
    # Users
    u1 = User.objects.create_user(username="user1", email="test1@test.com", password="password")
    u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password")
    u3 = User.objects.create_user(username="user3", email="test3@test.com", password="password")

    # Categories
    c1 = Category.objects.create(name="Antiques")
    c2 = Category.objects.create(name="Art")
    c3 = Category.objects.create(name="Baby")
    c4 = Category.objects.create(name="Books")
    c5 = Category.objects.create(name="Business & Industrial")
    c6 = Category.objects.create(name="Cameras & Photos")
    c7 = Category.objects.create(name="Celle Phones & Accessories")
    c8 = Category.objects.create(name="Clothing, Shoes & Accessories")
    c9 = Category.objects.create(name="Coins & Paper Money")
    c10 = Category.objects.create(name="Collectibles")
    c11 = Category.objects.create(name="Computer/Tablets & Networking")
    c12 = Category.objects.create(name="Consumer Electronics")
    c13 = Category.objects.create(name="Crafts")
    c14 = Category.objects.create(name="Dolls & Bears")
    c15 = Category.objects.create(name="DVDs & Movies")
    c16 = Category.objects.create(name="Gift Cards, Coupons & Tickets")
    c17 = Category.objects.create(name="Health & Beauty")
    c18 = Category.objects.create(name="Home & Garden")
    c19 = Category.objects.create(name="Jewerly & Watches")
    c20 = Category.objects.create(name="Jobs & Services")
    c21 = Category.objects.create(name="Music")
    c22 = Category.objects.create(name="Musical Instruments")
    c23 = Category.objects.create(name="Gear")
    c24 = Category.objects.create(name="Pet Supplies")
    c25 = Category.objects.create(name="Pottery & Glass")
    c26 = Category.objects.create(name="Sporting Goods")
    c27 = Category.objects.create(name="Toys & Hobbies")
    c28 = Category.objects.create(name="Travel")
    c29 = Category.objects.create(name="Vehicles, Auto, Moto")
    c30 = Category.objects.create(name="Video Games & Consoles")
    c31 = Category.objects.create(name="Everything else")

    # Items
    i1 = create_item(c8, u1, name="Shoes", description="My old shoes", price_min=10, price_max=30)
    i2 = create_item(c8, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30)
    i3 = create_item(c19, u1, name="Ring", description="My precious", price_min=100, price_max=500)
    i4 = create_item(c12, u2, name="New mouse", description="Brand new", price_min=20, price_max=100)
    i5 = create_item(c22, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000)

    # image = ImagePil.new('RGBA', size=(640, 960), color=(155, 0, 0))
    # file = tempfile.NamedTemporaryFile(suffix='.png')
    # image.save('test.png')
    # Image.objects.create(item=i1, image='test.png')

    # Create new offers with corresponding notifications (made automatically)
    o1 = create_offer(i1, i4)
    o2 = create_offer(i2, i5)
    o3 = create_offer(i3, i4)
    o4 = create_offer(i5, i2)

    # Change read to True for new offers notifications 2 and 4
    n2 = Notification.objects.get(pk=2)
    n2.read = True
    n2.save()
    n4 = Notification.objects.get(pk=4)
    n4.read = True
    n4.save()

    # Change status and accepted values for offers with the creation of corresponding notifications (made
    # automatically)
    o1.status = True
    o1.accepted = True
    o1.save()
    o2.status = True
    o2.accepted = True
    o2.save()
    o3.status = True
    o3.accepted = False
    o3.save()
    o4.status = True
    o4.accepted = True
    o4.save()

    # Change read to True for new accepted offer notification 5 and for new refused offer notification 7
    # n5 = Notification.objects.get(pk=5)
    # n5.read = True
    # n5.save()
    # n7 = Notification.objects.get(pk=7)
    # n7.read = True
    # n7.save()

    # Create new comments with corresponding notifications (made automatically)
    # co1 = create_comment(u1, i4)
    # co2 = create_comment(u1, i5)
    # co3 = create_comment(u2, i1)
    # co4 = create_comment(u2, i2)
    #
    # # Change read to True for new comments notifications 9 and 10
    # n9 = Notification.objects.get(pk=9)
    # n9.read = True
    # n9.save()
    # n10 = Notification.objects.get(pk=10)
    # n10.read = True
    # n10.save()
    #
    # # Create new notes with corresponding notifications (made automatically)
    # no1 = Note.objects.create(user=u2, offer=o1, text="Very good", note=5)
    # no2 = Note.objects.create(user=u2, offer=o2, text="Very bad", note=0)
    # no3 = Note.objects.create(user=u1, offer=o4, text="Not bad", note=2)
    #
    # # Change read to True for new note notification 14
    # n13 = Notification.objects.get(pk=14)
    # n13.read = True
    # n13.save()
