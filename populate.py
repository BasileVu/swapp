import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swapp.settings")

import django
from PIL import Image as ImagePil

django.setup()

from users.models import *
from items.models import *
from comments.models import Comment
from notifications.models import Notification


def create_item(category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0, views=0):
    return Item.objects.create(name=name, description=description, price_min=price_min,
                               price_max=price_max, archived=archived, category=category, owner=owner, views=views)


def create_offer(item_given, item_received, comment="Offer test"):
    return Offer.objects.create(item_given=item_given, item_received=item_received, comment=comment)


def create_comment(user, item, content="Comment test"):
    return Comment.objects.create(content=content, user=user, item=item)


if __name__ == '__main__':
    # Users
    u1 = User.objects.create_user(username="user1", email="test1@test.com", password="password")
    u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password")
    u3 = User.objects.create_user(username="user3", email="test3@test.com", password="password")
    u4 = User.objects.create_user(username="user4", email="test4@test.com", password="password")

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
    i1 = create_item(c8, u1, name="Shoes", description="My collector shoes", price_min=10, price_max=50, views=800)
    i2 = create_item(c8, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30, views=100)
    i3 = create_item(c19, u1, name="Ring", description="My precious", price_min=100, price_max=500, views=400)
    i4 = create_item(c12, u2, name="New mouse", description="Brand new", price_min=40, price_max=150, views=200)
    i5 = create_item(c22, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000,
                     views=1000)
    i6 = create_item(c22, u3, name="Violin", description="In good shape", price_min=1000, price_max=2000, views=30)
    i7 = create_item(c22, u3, name="Flute", description="Very old", price_min=200, price_max=300, views=40)
    i8 = create_item(c22, u3, name="Electric guitar", description="One cord is broken", price_min=150, price_max=250, views=50)
    i9 = create_item(c22, u4, name="Trumpet", description="Good sound", price_min=300, price_max=350, views=60)

    # Key info on items
    i1.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="Adidum"))
    i1.keyinfo_set.add(KeyInfo.objects.create(key="Size", info="40"))
    i1.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="Purple"))
    i2.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="Niko"))
    i2.keyinfo_set.add(KeyInfo.objects.create(key="Size", info="L"))
    i2.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="White"))
    i3.keyinfo_set.add(KeyInfo.objects.create(key="Made in", info="Mordor"))
    i3.keyinfo_set.add(KeyInfo.objects.create(key="Manufacturer", info="Sauron"))
    i3.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="Golden"))
    i4.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="LogicTe"))
    i4.keyinfo_set.add(KeyInfo.objects.create(key="Hand", info="Left"))
    i4.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="Black and white"))
    i5.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="StenStay"))
    i5.keyinfo_set.add(KeyInfo.objects.create(key="Hand", info="Left and right"))
    i5.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="Black"))
    i6.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="StradiWarior"))
    i6.keyinfo_set.add(KeyInfo.objects.create(key="Mater", info="Wood"))
    i6.keyinfo_set.add(KeyInfo.objects.create(key="Quality", info="Brand new"))
    i7.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="Pan"))
    i7.keyinfo_set.add(KeyInfo.objects.create(key="Quality", info="Bad shape"))
    i7.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="White"))
    i8.keyinfo_set.add(KeyInfo.objects.create(key="Brand", info="Power"))
    i8.keyinfo_set.add(KeyInfo.objects.create(key="Manufacturer", info="Elvis"))
    i8.keyinfo_set.add(KeyInfo.objects.create(key="Color", info="Blue ocean"))
    i9.keyinfo_set.add(KeyInfo.objects.create(key="Sound", info="Pouette"))
    i9.keyinfo_set.add(KeyInfo.objects.create(key="Quality", info="Good shape"))
    i9.keyinfo_set.add(KeyInfo.objects.create(key="Made in", info="China"))

    # Likes on items for users
    Like.objects.create(user=u2, item=i1)
    Like.objects.create(user=u3, item=i1)
    Like.objects.create(user=u4, item=i1)
    Like.objects.create(user=u2, item=i2)
    Like.objects.create(user=u3, item=i2)
    Like.objects.create(user=u3, item=i3)
    Like.objects.create(user=u1, item=i4)
    Like.objects.create(user=u3, item=i4)
    Like.objects.create(user=u4, item=i4)
    Like.objects.create(user=u4, item=i5)
    Like.objects.create(user=u1, item=i5)
    Like.objects.create(user=u4, item=i6)
    Like.objects.create(user=u4, item=i7)
    Like.objects.create(user=u1, item=i7)
    Like.objects.create(user=u2, item=i7)
    Like.objects.create(user=u2, item=i8)
    Like.objects.create(user=u3, item=i9)
    Like.objects.create(user=u1, item=i9)

    # image = ImagePil.new('RGBA', size=(640, 960), color=(155, 0, 0))
    # file = tempfile.NamedTemporaryFile(suffix='.png')
    # image.save('test.png')
    # Image.objects.create(item=i1, image='test.png')

    # Create new offers with corresponding notifications (made automatically)
    o1 = create_offer(i1, i4, "A good offer for my shoes")
    o2 = create_offer(i5, i6, "A very good offer my piano")
    o3 = create_offer(i3, i4, "A very very good offer for my old ring")
    o4 = create_offer(i7, i9, "Please accept my offer for my flute")
    o5 = create_offer(i5, i3, "I want your precious ring")

    # Change read to True for new offers notifications 2 and 4
    n2 = Notification.objects.get(pk=2)
    n2.read = True
    n2.save()
    n4 = Notification.objects.get(pk=4)
    n4.read = True
    n4.save()

    # Change status and accepted values for offers with the creation of corresponding notifications (made
    # automatically)
    o1.answered = True
    o1.accepted = True
    o1.save()
    o2.answered = True
    o2.accepted = True
    o2.save()
    o3.answered = True
    o3.accepted = False
    o3.save()
    o4.answered = True
    o4.accepted = True
    o4.save()

    # Change read to True for new accepted offer notification 6 and for new refused offer notification 8
    n6 = Notification.objects.get(pk=6)
    n6.read = True
    n6.save()
    n8 = Notification.objects.get(pk=8)
    n8.read = True
    n8.save()

    # Create new comments with corresponding notifications (made automatically)
    co1 = create_comment(u1, i4, "I think this mouse is not a good deal.")
    co2 = create_comment(u1, i5, "In my opinion, a piano can't be traded.")
    co3 = create_comment(u2, i1, "Oh, this old shoes are so rare.")
    co4 = create_comment(u2, i2, "Seriously, i don't think we can trade an old shirt. That is too ugly.")
    co5 = create_comment(u3, i1, "Aren't those the shoes of a famous football player?")
    co6 = create_comment(u3, i1, "But still, those shoes look smelly.")
    co7 = create_comment(u4, i1, "I want to put those shoes on.")

    # Change read to True for new comments notifications 10 and 11
    n10 = Notification.objects.get(pk=10)
    n10.read = True
    n10.save()
    n11 = Notification.objects.get(pk=11)
    n11.read = True
    n11.save()

    # Create new notes with corresponding notifications (made automatically)
    no1 = Note.objects.create(user=u2, offer=o1, text="Very good", note=5)
    no2 = Note.objects.create(user=u2, offer=o2, text="Very bad", note=0)
    no3 = Note.objects.create(user=u1, offer=o4, text="Not too bad", note=3)

    # Change read to True for new note notification 17
    n17 = Notification.objects.get(pk=17)
    n17.read = True
    n17.save()
