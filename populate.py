import os

from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swapp.settings")

import django

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


def set_image_profile(user, image_name):
    image = open("populate_images/profiles/profile_%s" % image_name, "rb")
    user.userprofile.image = File(image)
    user.userprofile.save()


def set_image_item(item, image_name):
    image = open("populate_images/items/item_%s" % image_name, "rb")
    Image.objects.create(image=File(image), item=item)


if __name__ == "__main__":
    # Users
    u1 = User.objects.create_user(username="user1", first_name="François", last_name="LePoulpe", email="test1@test.com",
                                  password="password")
    u2 = User.objects.create_user(username="user2", first_name="Marguerite", last_name="Ducosset",
                                  email="test2@test.com", password="password")
    u3 = User.objects.create_user(username="user3", first_name="Jack", last_name="Ometti", email="test3@test.com",
                                  password="password")
    u4 = User.objects.create_user(username="user4", first_name="Ania", last_name="Mongrito", email="test4@test.com",
                                  password="password")
    u5 = User.objects.create_user(username="user5", first_name="Jean", last_name="Duroux", email="test5@test.com",
                                  password="password")
    u6 = User.objects.create_user(username="user6", first_name="Claudine", last_name="Michel", email="test6@test.com",
                                  password="password")

    # Add locations to users
    u1.location.street = "Route de Cheseaux 1"
    u1.location.city = "Yverdon-les-Bains"
    u1.location.region = "VD"
    u1.location.country = "Switzerland"
    u1.location.save()

    u2.location.street = "Limmatstrasse 23"
    u2.location.city = "Zürich"
    u2.location.region = "ZH"
    u2.location.country = "Switzerland"
    u2.location.save()

    u3.location.street = "17 Boulevard de Vaugirard"
    u3.location.city = "Paris"
    u3.location.region = "Île-de-France"
    u3.location.country = "France"
    u3.location.save()

    u4.location.street = "385 Route de Meyrin"
    u4.location.city = "Meyrin"
    u4.location.region = "GE"
    u4.location.country = "Switzerland"
    u4.location.save()

    u5.location.street = "85 quai d'Austerlitz"
    u5.location.city = "Paris"
    u5.location.region = "Île-de-France"
    u5.location.country = "France"
    u5.location.save()

    u6.location.street = "Place Pestalozzi 14"
    u6.location.city = "Yverdon-les-Bains"
    u6.location.region = "VD"
    u6.location.country = "Switzerland"
    u6.location.save()

    # Add coordinates to users
    u1.coordinates.latitude = 46.7793801
    u1.coordinates.longitude = 6.659497600000001
    u1.coordinates.save()

    u2.coordinates.latitude = 47.380754
    u2.coordinates.longitude = 8.5365015
    u2.coordinates.save()

    u3.coordinates.latitude = 48.8407963
    u3.coordinates.longitude = 2.3201484
    u3.coordinates.save()

    u4.coordinates.latitude = 46.2337481
    u4.coordinates.longitude = 6.0523948
    u4.coordinates.save()

    u5.coordinates.latitude = 48.8419695
    u5.coordinates.longitude = 2.3665938
    u5.coordinates.save()

    u6.coordinates.latitude = 46.77866239999999
    u6.coordinates.longitude = 6.6419655
    u6.coordinates.save()

    # Categories
    c1 = Category.objects.create(name="Antiques")
    c2 = Category.objects.create(name="Art")
    c3 = Category.objects.create(name="Baby")
    c4 = Category.objects.create(name="Books")
    c5 = Category.objects.create(name="Business & Industrial")
    c6 = Category.objects.create(name="Cameras & Photos")
    c7 = Category.objects.create(name="Cell Phones & Accessories")
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

    # Delivery methods
    DeliveryMethod.objects.create(name="At my place")
    DeliveryMethod.objects.create(name="At any place")
    DeliveryMethod.objects.create(name="By mail")

    # Items
    i1 = create_item(c8, u1, name="Shoes", description="My collector shoes", price_min=10, price_max=50, views=800)
    i2 = create_item(c8, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30, views=100)
    i3 = create_item(c19, u1, name="Ring", description="My precious", price_min=100, price_max=500, views=400)

    i4 = create_item(c12, u2, name="New mouse", description="Brand new", price_min=40, price_max=150, views=200)
    i5 = create_item(c22, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000,
                     views=1000)

    i6 = create_item(c22, u3, name="Violin", description="In good shape", price_min=1000, price_max=2000, views=30)
    i7 = create_item(c22, u3, name="Flute", description="Very old", price_min=200, price_max=300, views=40)
    i8 = create_item(c22, u3, name="Electric guitar", description="One cord is broken", price_min=150, price_max=250,
                     views=50)

    i9 = create_item(c22, u4, name="Trumpet", description="Good sound", price_min=300, price_max=350, views=60)

    # Set userprofiles images
    set_image_profile(u1, "user1.jpg")
    set_image_profile(u2, "user2.jpg")
    set_image_profile(u3, "user3.jpg")
    set_image_profile(u4, "user4.jpg")
    set_image_profile(u5, "user5.jpg")
    set_image_profile(u6, "user6.jpg")

    # Set items images
    set_image_item(i1, "shoes_1.jpg")
    set_image_item(i1, "shoes_2.jpg")
    set_image_item(i1, "shoes_3.jpg")

    set_image_item(i2, "shirt_1.jpg")
    set_image_item(i2, "shirt_2.jpg")

    set_image_item(i3, "ring_1.jpg")

    set_image_item(i4, "newMouse_1.jpg")
    set_image_item(i4, "newMouse_2.png")
    set_image_item(i4, "newMouse_3.jpg")

    set_image_item(i5, "piano_1.png")
    set_image_item(i5, "piano_2.jpg")

    set_image_item(i6, "violin_1.jpg")

    set_image_item(i7, "flute_1.jpg")
    set_image_item(i7, "flute_2.jpg")
    set_image_item(i7, "flute_3.jpg")

    set_image_item(i8, "electricGuitar_1.jpg")
    set_image_item(i8, "electricGuitar_2.jpg")

    set_image_item(i9, "trumpet_1.jpg")
    set_image_item(i9, "trumpet_2.jpg")
    set_image_item(i9, "trumpet_3.jpg")

    # Key info on items
    KeyInfo.objects.create(key="Brand", info="Adidum", item=i1)
    KeyInfo.objects.create(key="Size", info="40", item=i1)
    KeyInfo.objects.create(key="Color", info="Purple", item=i1)

    KeyInfo.objects.create(key="Brand", info="Niko", item=i2)
    KeyInfo.objects.create(key="Size", info="L", item=i2)
    KeyInfo.objects.create(key="Color", info="White", item=i2)

    KeyInfo.objects.create(key="Made in", info="Mordor", item=i3)
    KeyInfo.objects.create(key="Manufacturer", info="Sauron", item=i3)
    KeyInfo.objects.create(key="Color", info="Golden", item=i3)

    KeyInfo.objects.create(key="Brand", info="LogicTe", item=i4)
    KeyInfo.objects.create(key="Hand", info="Left", item=i4)
    KeyInfo.objects.create(key="Color", info="Black and white", item=i4)

    KeyInfo.objects.create(key="Brand", info="StenStay", item=i5)
    KeyInfo.objects.create(key="Hand", info="Left and right", item=i5)
    KeyInfo.objects.create(key="Color", info="Black", item=i5)

    KeyInfo.objects.create(key="Brand", info="StradiWarior", item=i6)
    KeyInfo.objects.create(key="Mater", info="Wood", item=i6)
    KeyInfo.objects.create(key="Quality", info="Brand new", item=i6)

    KeyInfo.objects.create(key="Brand", info="Pan", item=i7)
    KeyInfo.objects.create(key="Quality", info="Bad shape", item=i7)
    KeyInfo.objects.create(key="Color", info="White", item=i7)

    KeyInfo.objects.create(key="Brand", info="Power", item=i8)
    KeyInfo.objects.create(key="Manufacturer", info="Elvis", item=i8)
    KeyInfo.objects.create(key="Color", info="Blue ocean", item=i8)

    KeyInfo.objects.create(key="Sound", info="Pouette", item=i9)
    KeyInfo.objects.create(key="Quality", info="Good shape", item=i9)
    KeyInfo.objects.create(key="Made in", info="China", item=i9)

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

    # Create new offers with corresponding notifications (made automatically)
    o1 = create_offer(i1, i4, "A good offer for my shoes")
    o2 = create_offer(i5, i6, "A very good offer my piano")
    o3 = create_offer(i3, i4, "A very very good offer for my old ring")
    o4 = create_offer(i7, i9, "Please accept my offer for my flute")
    # These offers will be not accepted or refused (not answered)
    o5 = create_offer(i5, i3, "I want your precious ring")
    o6 = create_offer(i8, i4, "I want your brand new mouse")

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
