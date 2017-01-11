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

    # Interested by categories
    u1.userprofile.categories.add(c8)
    u1.userprofile.categories.add(c14)
    u1.userprofile.categories.add(c16)
    u1.userprofile.categories.add(c25)
    u1.save()

    u2.userprofile.categories.add(c1)
    u2.userprofile.categories.add(c8)
    u2.userprofile.categories.add(c26)
    u2.userprofile.categories.add(c30)
    u2.userprofile.categories.add(c31)
    u2.save()

    u3.userprofile.categories.add(c3)
    u3.userprofile.categories.add(c4)
    u3.userprofile.categories.add(c5)
    u3.userprofile.categories.add(c15)
    u3.userprofile.categories.add(c16)
    u3.userprofile.categories.add(c26)
    u3.save()

    u4.userprofile.categories.add(c1)
    u4.userprofile.categories.add(c7)
    u4.userprofile.categories.add(c22)
    u4.userprofile.categories.add(c23)
    u4.userprofile.categories.add(c24)
    u4.userprofile.categories.add(c30)
    u4.save()

    u5.userprofile.categories.add(c11)
    u5.userprofile.categories.add(c18)
    u5.userprofile.categories.add(c23)
    u5.userprofile.categories.add(c30)
    u5.userprofile.categories.add(c31)
    u5.save()

    u6.userprofile.categories.add(c1)
    u6.userprofile.categories.add(c14)
    u6.userprofile.categories.add(c18)
    u6.save()

    # Delivery methods
    d1 = DeliveryMethod.objects.create(name="At my place")
    d2 = DeliveryMethod.objects.create(name="At any place")
    d3 = DeliveryMethod.objects.create(name="By mail")

    # Items
    i1 = create_item(c8, u1, name="Shoes", description="A shoe is an item of footwear intended to protect and comfort "
                                                       "the human foot while the wearer is doing various activities. "
                                                       "Shoes are also used as an item of decoration and fashion. The "
                                                       "design of shoes has varied enormously through time and from "
                                                       "culture to culture, with appearance originally being tied to "
                                                       "function."
                                                       "\n \n"
                                                       "Additionally, fashion has often dictated many "
                                                       "design elements, such as whether shoes have very high heels "
                                                       "or flat ones. Contemporary footwear in the 2010s varies "
                                                       "widely in style, complexity and cost. Basic sandals may "
                                                       "consist of only a thin sole and simple strap and be sold for "
                                                       "a low cost. High fashion shoes made by famous designers may "
                                                       "be made of expensive materials, use complex construction and "
                                                       "sell for hundreds or even thousands of dollars a pair."
                                                       "\n \n"
                                                       "Some shoes are designed for specific purposes, such as boots "
                                                       "designed specifically for mountaineering or skiing.",
                     price_min=10, price_max=50, views=800)
    i1.delivery_methods.add(d1)
    i1.delivery_methods.add(d2)
    i1.delivery_methods.add(d3)
    i1.save()
    i2 = create_item(c8, u1, name="Shirt", description="A shirt is a cloth garment for the upper body."
                                                       "\n \n"
                                                       "Originally an "
                                                       "undergarment worn exclusively by men and women it has become, "
                                                       "in American English, a catch-all term for a broad variety of "
                                                       "upper-body garments and undergarments. In British English, "
                                                       "a shirt is more specifically a garment with a collar, "
                                                       "sleeves with cuffs, and a full vertical opening with buttons "
                                                       "or snaps (North Americans would call that a 'dress shirt', "
                                                       "a specific type of 'collared shirt')."
                                                       "\n \n"
                                                       "A shirt can also be "
                                                       "worn with a necktie under the shirt collar.", price_min=5,
                     price_max=30, views=100)
    i2.delivery_methods.add(d1)
    i2.save()
    i3 = create_item(c19, u1, name="Ring", description="A ring is a round band, usually of metal, worn as an "
                                                       "ornamental piece of jewellery around the finger, or sometimes "
                                                       "the toe; it is the most common current meaning of the word "
                                                       "'ring'."
                                                       "\n \n"
                                                       "Strictly speaking a normal ring is a finger ring ("
                                                       "which may be hyphenated); other types of rings worn as "
                                                       "ornaments are earrings, bracelets for the wrist, armlets or "
                                                       "arm rings, toe rings and torc or neck rings, but except "
                                                       "perhaps for toe rings, the plain term 'ring' is not normally "
                                                       "used to refer to these."
                                                       "\n \n"
                                                       "Rings are most often made of metal "
                                                       "but can be of almost any material: metal, plastic, stone, "
                                                       "wood, bone, glass, or gemstone. They may be set with a stone "
                                                       "or stones, often a gemstone such as diamond, ruby, "
                                                       "sapphire or emerald.", price_min=100, price_max=500, views=400)
    i3.delivery_methods.add(d2)
    i3.delivery_methods.add(d3)
    i3.save()
    i4 = create_item(c12, u2, name="New mouse", description="A computer mouse is a pointing device (hand control) "
                                                            "that detects two-dimensional motion relative to a "
                                                            "surface."
                                                            "\n \n"
                                                            "This motion is typically translated into the "
                                                            "motion of a pointer on a display, which allows a smooth "
                                                            "control of the graphical user interface. Physically, "
                                                            "a mouse consists of an object held in one's hand, "
                                                            "with one or more buttons."
                                                            "\n \n"
                                                            "Mice often also feature other "
                                                            "elements, such as touch surfaces and 'wheels', "
                                                            "which enable additional control and dimensional input.",
                     price_min=40, price_max=150, views=200)
    i4.delivery_methods.add(d2)
    i4.save()
    i5 = create_item(c22, u2, name="Piano", description="The piano is an acoustic, stringed musical instrument, "
                                                        "in which the strings are struck by hammers. It is played "
                                                        "using a keyboard, which is a row of keys (small levers) "
                                                        "that the performer presses down or strikes with the fingers "
                                                        "and thumbs of both hands to cause the hammers to strike the "
                                                        "strings."
                                                        "\n \n"
                                                        "Invented in about 1700 (the exact year is "
                                                        "uncertain), the piano is widely employed in classical, jazz, "
                                                        "traditional and popular music for solo and ensemble "
                                                        "performances, accompaniment, and for composing, songwriting "
                                                        "and rehearsals."
                                                        ""
                                                        "\n \n"
                                                        "Although the piano is very heavy and thus "
                                                        "not portable and is expensive (in comparison with other "
                                                        "widely used accompaniment instruments, such as the acoustic "
                                                        "guitar), its musical versatility (i.e., its wide pitch "
                                                        "range, ability to play chords with up to 10 notes, "
                                                        "louder or softer notes and two or more independent musical "
                                                        "lines at the same time), the large number of musicians and "
                                                        "amateurs trained in playing it, and its wide availability in "
                                                        "performance venues, schools and rehearsal spaces have made "
                                                        "it one of the Western world's most familiar musical "
                                                        "instruments.", price_min=500, price_max=1000, views=1000)
    i5.delivery_methods.add(d1)
    i5.delivery_methods.add(d2)
    i5.delivery_methods.add(d3)
    i5.save()
    i6 = create_item(c22, u3, name="Violin", description="The violin is a wooden string instrument in the violin "
                                                         "family. It is the smallest and highest-pitched instrument "
                                                         "in the family in regular use. Smaller violin-type "
                                                         "instruments are known, including the violino piccolo and "
                                                         "the kit violin, but these are virtually unused in the "
                                                         "2010s."
                                                         "\n \n"
                                                         "The violin typically has four strings tuned in "
                                                         "perfect fifths, and is most commonly played by drawing a "
                                                         "bow across its strings, though it can also be played by "
                                                         "plucking the strings with the fingers (pizzicato). Violins "
                                                         "are important instruments in a wide variety of musical "
                                                         "genres."
                                                         "\n \n"
                                                         "They are most prominent in the Western classical "
                                                         "tradition and in many varieties of folk music. They are "
                                                         "also frequently used in genres of folk including country "
                                                         "music and bluegrass music and in jazz. Electric violins are "
                                                         "used in some forms of rock music; further, the violin has "
                                                         "come to be played in many non-Western music cultures, "
                                                         "including Indian music and Iranian music."
                                                         "\n \n"
                                                         "The violin is "
                                                         "sometimes informally called a fiddle, particularly in Irish "
                                                         "traditional music and bluegrass, but this nickname is also "
                                                         "used regardless of the type of music played on it.",
                     price_min=1000, price_max=2000, views=30)
    i6.delivery_methods.add(d1)
    i6.delivery_methods.add(d3)
    i6.save()
    i7 = create_item(c22, u3, name="Flute", description="The flute is a family of musical instruments in the woodwind "
                                                        "group. Unlike woodwind instruments with reeds, a flute is an "
                                                        "aerophone or reedless wind instrument that produces its "
                                                        "sound from the flow of air across an opening."
                                                        "\n \n"
                                                        "According to "
                                                        "the instrument classification of Hornbostel–Sachs, "
                                                        "flutes are categorized as edge-blown aerophones."
                                                        "\n \n"
                                                        "A musician who plays the flute can be referred to as a flute "
                                                        "player, flautist, flutist or, less commonly, "
                                                        "fluter or flutenist.",
                     price_min=200, price_max=300, views=40)
    i7.delivery_methods.add(d1)
    i7.delivery_methods.add(d2)
    i7.delivery_methods.add(d3)
    i7.save()
    i8 = create_item(c22, u3, name="Electric guitar", description="An electric guitar is a fretted string instrument "
                                                                  "that uses a pickup to convert the vibration of its "
                                                                  "strings—which are typically made of steel, "
                                                                  "and which occurs when a guitarist strums, "
                                                                  "plucks or fingerpicks the strings—into electrical "
                                                                  "signals."
                                                                  "\n \n"
                                                                  "The vibrations of the strings are sensed "
                                                                  "by a pickup, of which the most common type is the "
                                                                  "magnetic pickup, which uses the principle of "
                                                                  "direct electromagnetic induction. The signal "
                                                                  "generated by an electric guitar is too weak to "
                                                                  "drive a loudspeaker, so it is plugged into a "
                                                                  "guitar amplifier before being sent to a "
                                                                  "loudspeaker, which makes a sound loud enough to "
                                                                  "hear."
                                                                  "\n \n"
                                                                  "The output of an electric guitar is an "
                                                                  "electric signal, and the signal can easily be "
                                                                  "altered by electronic circuits to add 'color' to "
                                                                  "the sound or change the sound. Often the signal is "
                                                                  "modified using effects such as reverb and "
                                                                  "distortion and 'overdrive', with the latter being "
                                                                  "a key element of the sound of the electric guitar "
                                                                  "as it is used in blues and rock music.",
                     price_min=150, price_max=250, views=50)
    i8.delivery_methods.add(d1)
    i8.delivery_methods.add(d3)
    i8.save()
    i9 = create_item(c22, u4, name="Trumpet", description="A trumpet is a musical instrument commonly used in "
                                                          "classical and jazz ensembles. The trumpet group contains "
                                                          "the instruments with the highest register in the brass "
                                                          "family. Trumpet-like instruments have historically been "
                                                          "used as signaling devices in battle or hunting, "
                                                          "with examples dating back to at least 1500 BC; they began "
                                                          "to be used as musical instruments only in the late-14th or "
                                                          "early 15th century."
                                                          "\n \n"
                                                          "Trumpets are used in art music "
                                                          "styles, for instance in orchestras, concert bands, "
                                                          "and jazz ensembles, as well as in popular music. They are "
                                                          "played by blowing air through almost-closed lips (called "
                                                          "the player's embouchure), producing a 'buzzing' sound that "
                                                          "starts a standing wave vibration in the air column inside "
                                                          "the instrument."
                                                          "\n \n"
                                                          "Since the late 15th century they have "
                                                          "primarily been constructed of brass tubing, usually bent "
                                                          "twice into a rounded rectangular shape.", price_min=300,
                     price_max=350, views=60)
    i9.delivery_methods.add(d3)
    i9.save()

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
    set_image_item(i2, "shirt_3.jpg")

    set_image_item(i3, "ring_1.jpg")
    set_image_item(i3, "ring_2.jpg")
    set_image_item(i3, "ring_3.jpg")

    set_image_item(i4, "newMouse_1.jpg")
    set_image_item(i4, "newMouse_2.jpg")
    set_image_item(i4, "newMouse_3.jpg")

    set_image_item(i5, "piano_1.jpg")
    set_image_item(i5, "piano_2.jpg")
    set_image_item(i5, "piano_3.jpg")

    set_image_item(i6, "violin_1.jpg")
    set_image_item(i6, "violin_2.jpg")
    set_image_item(i6, "violin_3.jpg")

    set_image_item(i7, "flute_1.jpg")
    set_image_item(i7, "flute_2.jpg")
    set_image_item(i7, "flute_3.jpg")

    set_image_item(i8, "electricGuitar_1.jpg")
    set_image_item(i8, "electricGuitar_2.jpg")
    set_image_item(i8, "electricGuitar_3.jpg")

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
    o1 = create_offer(i1, i4, "A good offer for my shoes.")
    o2 = create_offer(i5, i6, "A very good offer my piano.")
    o3 = create_offer(i3, i4, "A very very good offer for my old ring.")
    o4 = create_offer(i7, i9, "Please accept my offer for my flute.")
    # These offers will be not accepted or refused (not answered)
    o5 = create_offer(i5, i3, "I want your precious ring.")
    o6 = create_offer(i8, i4, "I want your brand new mouse.")

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

    # Change read to True for new accepted offer notification 7 and for new refused offer notification 9
    n7 = Notification.objects.get(pk=7)
    n7.read = True
    n7.save()

    n9 = Notification.objects.get(pk=9)
    n9.read = True
    n9.save()

    # Create new comments with corresponding notifications (made automatically)
    co1 = create_comment(u2, i1, "Oh, this old shoes are so rare.")
    co2 = create_comment(u3, i1, "Aren't those the shoes of a famous football player?")
    co3 = create_comment(u4, i1, "But still, those shoes look smelly.")
    co4 = create_comment(u5, i1, "I want to put those shoes on.")

    co5 = create_comment(u1, i2, "I don't want this ugly shirt.")
    co6 = create_comment(u4, i2, "I really need a shirt like this.")
    co7 = create_comment(u5, i2, "This shirt is too expensive.")
    co8 = create_comment(u6, i2, "Oh, this shirt has a nice color.")

    co9 = create_comment(u2, i3, "I need the precious.")
    co10 = create_comment(u3, i3, "I know the manufacturer of this ring.")
    co11 = create_comment(u4, i3, "This ring reminds me of a film.")

    co12 = create_comment(u1, i4, "I think this mouse is not a good deal.")
    co13 = create_comment(u2, i4, "I really need a mouse like this.")
    co14 = create_comment(u6, i4, "This mouse seems to break down.")

    co15 = create_comment(u3, i5, "In my opinion, a piano can't be traded.")
    co16 = create_comment(u4, i5, "A piano is too big to be traded.")
    co17 = create_comment(u5, i5, "This piano is too expensive.")

    co18 = create_comment(u2, i6, "This violin could be a big deal.")
    co19 = create_comment(u3, i6, "This violin comes from a well know manufacturer.")
    co20 = create_comment(u5, i6, "I don't really want a violin like this.")

    co21 = create_comment(u1, i7, "This instrument could be a big deal.")
    co22 = create_comment(u3, i7, "This flute comes from a well know manufacturer.")
    co23 = create_comment(u5, i7, "That is a good deal.")

    co24 = create_comment(u1, i8, "I need a new guitar.")
    co25 = create_comment(u3, i8, "This guitar is not very expensive.")
    co26 = create_comment(u4, i8, "I'm looking for a guitar like this.")

    co27 = create_comment(u1, i9, "I need a new trumpet.")
    co28 = create_comment(u2, i9, "This is a very good trumpet.")
    co29 = create_comment(u3, i9, "I'm looking for a trumpet like this.")

    # Change read to True for new comments notifications 11, 12, 15 and 16
    n11 = Notification.objects.get(pk=11)
    n11.read = True
    n11.save()

    n12 = Notification.objects.get(pk=12)
    n12.read = True
    n12.save()

    n15 = Notification.objects.get(pk=15)
    n15.read = True
    n15.save()

    n16 = Notification.objects.get(pk=16)
    n16.read = True
    n16.save()

    # Create new notes with corresponding notifications (made automatically)
    no1 = Note.objects.create(user=u1, offer=o1, text="Very good", note=5)
    no2 = Note.objects.create(user=u2, offer=o1, text="Not very good", note=3)

    no3 = Note.objects.create(user=u2, offer=o2, text="Bad", note=1)
    no4 = Note.objects.create(user=u3, offer=o2, text="Not recommended", note=0)

    no5 = Note.objects.create(user=u3, offer=o4, text="Not too bad", note=2)
    no6 = Note.objects.create(user=u4, offer=o4, text="Excellent transaction", note=5)

    # Change read to True for new note notification 40 and 42
    n40 = Notification.objects.get(pk=40)
    n40.read = True
    n40.save()

    n42 = Notification.objects.get(pk=42)
    n42.read = True
    n42.save()
