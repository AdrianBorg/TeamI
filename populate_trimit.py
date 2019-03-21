import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TeamI.settings')
import django
django.setup()
from trimit.models import Page, UserProfile, Review, UserHairImage, PageImage, Treatment, Specialities
# from trimit.models import EUser as User
from django.contrib.auth.models import User
from django.conf import settings
from django_countries import countries
from django.core.files import File
import os

POPULATE_DIR = os.path.join(settings.STATIC_DIR, 'population')
review_pictures_dir = os.path.join(POPULATE_DIR, 'review_pictures')
profile_pic_dir = os.path.join(POPULATE_DIR, 'profile_pictures')


def populate():

    stylists = [
        {
            "username": "stylist1",
            "email": "stylist1@trimit.com",
        },
        {
            "username": "stylist2",
            "email": "stylist2@trimit.com",
        },
        {
            "username": "stylist3",
            "email": "stylist3@trimit.com",
        },
        {
            "username": "stylist4",
            "email": "stylist4@trimit.com",
        },
        {
            "username": "stylist5",
            "email": "stylist5@trimit.com",
        },
        {
            "username": "stylist6",
            "email": "stylist6@trimit.com",
        },
        {
            "username": "stylist7",
            "email": "stylist7@trimit.com",
        },
        {
            "username": "stylist8",
            "email": "stylist8@trimit.com",
        },
        {
            "username": "stylist9",
            "email": "stylist9@trimit.com",
        },
        {
            "username": "stylist10",
            "email": "stylist10@trimit.com",
        },
        {
            "username": "stylist11",
            "email": "stylist11@trimit.com",
        },
        {
            "username": "stylist12",
            "email": "stylist12@trimit.com",
        }
    ]

    users = [
        {
            "username": "user1",
            "email": "user1@trimit.com",
            "favourites": [stylists[0]['username'],
                           stylists[2]['username'],
                           stylists[8]['username'],
                           stylists[9]['username'], ]
        },
        {
            "username": "user2",
            "email": "user2@trimit.com",
            "favourites": None,
        },
        {
            "username": "user3",
            "email": "user3@trimit.com",
            "favourites": None,
        },
        {
            "username": "user4",
            "email": "user4@trimit.com",
            "favourites": None,
        },
    ]

    deleting_users = [
        {
            "username": "user4",
        },
    ]

    hairdresser_pages = [
        {
            "name": "Hanna",
            "str": "1 Argyle Str",
            "city": "Glasgow",
            "country": "GB",
            "times": "9 to 5 all week",
            "contact_no": "+44 4444 555 666",
            "description": "We cut hair, been doing it for 20 years. We pride ourselves in giving the best service we can!",
            "picture": 'stylistPic.png',
            "specialities": ['curly', 'red', 'dye', 'black', ],
            "website": "hanna.co.uk",
            "ig": "instagram.com/hanna",
        },
        {
            "name": "BubbleBath",
            "str": "5 Bath Str",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": ['dye', 'colourful', ],
            "website": None,
            "ig": None,
        },
        {
            "name": "Clint Eastwood",
            "str": "50 Great Western Road",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": ['curly', 'straight', 'extensions', ],
            "website": None,
            "ig": None,
        },
        {
            "name": "fortune",
            "str": "90 triq il-kbira",
            "city": "Siggiewi",
            "country": "MT",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "HairyMary",
            "str": "50 Bothwell Street",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": ['straight', 'short', ],
            "website": None,
            "ig": None,
        },
        {
            "name": "Cuts",
            "str": "90 Elmbank Street",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Snippy",
            "str": "54 Napiershall Street",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Dye Another Day",
            "str": "65 Highburgh Road",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Shear Excellence",
            "str": "753 Govan Road",
            "city": "Glasgow",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Royal Snips",
            "str": "Queen Street",
            "city": "Edinburgh",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Antonios",
            "str": "100 Grey Street",
            "city": "Newcastle",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        },
        {
            "name": "Deenies",
            "str": "13 Summerfield Terrace",
            "city": "Aberdeen",
            "country": "GB",
            "times": None,
            "contact_no": None,
            "description": None,
            "picture": None,
            "specialities": None,
            "website": None,
            "ig": None,
        }
    ]

    reviews = [
        {
            "user": users[0]["username"],
            "page": stylists[0]["username"],
            "rating": (5.0, 4.5, 3.2),
            "comment": "Nice place, great atmosphere",
            "img": 'revpic.jpg',
        },
        {
            "user": users[1]["username"],
            "page": stylists[1]["username"],
            "rating": (3.5, 2.2, 5),
            "comment": "Bit expensive, but they were very friendly",
            "img": 'Blonde3.jpg',
        },
        {
            "user": users[2]["username"],
            "page": stylists[0]["username"],
            "rating": (4.5, 4.6, 4),
            "comment": "No major complaints",
            "img": 'Blonde.jpg',
        },
        {
            "user": users[0]["username"],
            "page": stylists[1]["username"],
            "rating": (2.7, 3.5, 4.8),
            "comment": "Super friendly, but could be cleaner",
            "img": 'Blonde2.jpg',
        },
        {
            "user": users[0]["username"],
            "page": stylists[2]["username"],
            "rating": (3.2, 1.5, 1),
            "comment": "Do not recommend, too expensive and bad service too",
            "img": None,
        },
        {
            "user": users[1]["username"],
            "page": stylists[4]["username"],
            "rating": (1.6, 4.4, 1.0),
            "comment": "deletedtest5",
            "img": None,
        },
        {
            "user": users[0]["username"],
            "page": stylists[5]["username"],
            "rating": (3.6, 2.6, 5),
            "comment": "Nice people, but a bit expensive",
            "img": None,
        },
        {
            "user": users[1]["username"],
            "page": stylists[6]["username"],
            "rating": (4.3, 4.4, 1.0),
            "comment": "Very rude, but everything is good",
            "img": None,
        },
        {
            "user": users[2]["username"],
            "page": stylists[7]["username"],
            "rating": (3.5, 4.3, 4),
            "comment": "Nice place",
            "img": None,
        },
        {
            "user": users[3]["username"],
            "page": stylists[8]["username"],
            "rating": (3, 2, 1),
            "comment": "Did not like this place",
            "img": None,
        },
        {
            "user": users[0]["username"],
            "page": stylists[0]["username"],
            "rating": (5, 5, 5),
            "comment": "Very happy with this place",
            "img": None,
        },
        {
            "user": users[1]["username"],
            "page": stylists[7]["username"],
            "rating": (2, 2, 2),
            "comment": "Did not like this place",
            "img": None,
        }
    ]

    hairdresser_treatments = [
        {
            "hairdresser_slug": "stylist4",
            "description": "hair dye",
            "price": "25£",
        },
        {
            "hairdresser_slug": "stylist4",
            "description": "head massage",
            "price": "35£/h",
        },
        {
            "hairdresser_slug": "stylist1",
            "description": "hair dye",
            "price": "30£",
        },
    ]


    profile_pictures = {
        "dir": os.path.join(POPULATE_DIR, 'profile_pictures'),
        "pic": [
            {
                'user': users[0]['username'],
                'img': 'user1.png',
            },
            {
                'user': users[1]['username'],
                'img': 'user2.png',
            },
        ]
    }

    hair_pictures = {
        "dir": os.path.join(POPULATE_DIR, 'hair_pictures'),
        "pic": [
            {
                'user': users[0]['username'],
                'img': 'Blonde.jpg',
            },
            {
                'user': users[0]['username'],
                'img': 'Blonde2.jpg',
            },
            {
                'user': users[0]['username'],
                'img': 'Blonde3.jpg',
            },
        ]
    }

    page_pictures = {
        "dir": os.path.join(POPULATE_DIR, 'page_pictures'),
        "pic": [
            {
                'user': stylists[0]['username'],
                'img': 'page1.jpg',
            },
            {
                'user': stylists[0]['username'],
                'img': 'page2.jpg',
            },
            {
                'user': stylists[0]['username'],
                'img': 'page3.jpg',
            },
        ]
    }

    def add_user(username, email):
        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password("technology")
        if created:
            user.save()

    def add_userprofile(us):
        user = User.objects.get(username=us['username'])
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.save()

        if us['favourites'] is not None:
            for tag in us['favourites']:
                p = Page.objects.get(user=User.objects.get(username=tag))
                profile.favourites.add(p)

    def get_standardized_country(country):
        for c in list(countries):
            if country.lower() == c[1].lower() or country.lower == c[0].lower:
                matched_country = country
        return matched_country

    def add_page(username, hairdresser):
        user = User.objects.get(username=username)

        standardized_country = get_standardized_country(hairdresser['country'])

        page_info = dict(
            name=hairdresser['name'],
            street_address=hairdresser['str'], 
            city=hairdresser['city'], 
            country=standardized_country,
            opening_times=hairdresser['times'],
            contact_number=hairdresser['contact_no'],
            description=hairdresser['description'],
            webpage=hairdresser['website'],
            instagram=hairdresser['ig'],
        )

        page = Page.objects.update_or_create(
            user=user, 
            defaults=page_info,
        )[0]

        if hairdresser['picture'] is not None:
            filedir = os.path.join(profile_pic_dir, hairdresser['picture'])
            page.profile_picture.save(hairdresser['picture'], File(open(filedir, 'rb')))

        page.save()

        if hairdresser['specialities'] is not None:
            for tag in hairdresser['specialities']:
                speciality = Specialities.objects.get_or_create(name=tag)[0]
                page.specialities.add(speciality)

    def add_review(username, pagename, ratings, comment, img):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        page = Page.objects.get(user=User.objects.get(username=pagename))
        atmosphere_rating, price_rating, service_rating = ratings
        review = Review.objects.get_or_create(
            page=page, user=user, atmosphere_rating=atmosphere_rating, 
            price_rating=price_rating, service_rating=service_rating,
            comment=comment
            )[0]
        if img is not None:
            filedir = os.path.join(review_pictures_dir, img)
            review.picture.save(img, File(open(filedir, 'rb')))

        review.save()

    def delete_user(username):
        user = User.objects.get(username=username)
        user.delete()

    def add_profile_picture(dir, username, filename):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        filedir = os.path.join(dir, filename)
        user.profile_picture.save(filename, File(open(filedir, 'rb')))

    def add_hair_picture(dir, username, filename):
        filedir = os.path.join(dir, filename)
        hairimage = UserHairImage.objects.create(user=UserProfile.objects.get(user=User.objects.get(username=username)))
        hairimage.image.save(filename, File(open(filedir, 'rb')))
        hairimage.save()

    def add_page_picture(dir, username, filename):
        filedir = os.path.join(dir, filename)
        pageimage = PageImage.objects.create(page=Page.objects.get(user=User.objects.get(username=username)))
        pageimage.image.save(filename, File(open(filedir, 'rb')))
        pageimage.save()

    def delete_duplicatable_objects():
        hairimages = UserHairImage.objects.all()
        pageimages = PageImage.objects.all()
        reviews = Review.objects.filter(user__isnull=True)

        for hi in hairimages:
            hi.delete()

        for pi in pageimages:
            pi.delete()

        for r in reviews:
            r.delete()

    delete_duplicatable_objects()

    i = 0

    for hs in stylists:
        add_user(hs['username'], hs['email'])
        hairdresser = hairdresser_pages[i]
        u = User.objects.get(username=hs['username'])
        add_page(u, hairdresser)
        i += 1

    for us in users:
        add_user(us['username'], us['email'])
        add_userprofile(us)

    for rev in reviews:
        add_review(rev['user'], rev['page'], rev['rating'], rev['comment'], rev['img'])

    for u in User.objects.all():
        for p in UserProfile.objects.filter(user=u):
            print("- {0} - UserProfile {1}".format(str(u), str(p)))
            for r in Review.objects.filter(user=UserProfile.objects.filter(user=u)):
                print("\t - Review {0}".format(str(r)))
        for p in Page.objects.filter(user=u):
            print("- {0} - HairdresserPage {1}".format(str(u), str(p)))
        for p in Page.objects.filter(user=u):
            for r in Review.objects.filter(page=p):
                print("\t- Review {0}".format(str(r)))

    for u in deleting_users:
        delete_user(username=u['username'])
        print("- DELETED - {0}".format(u['username']))

    for pp in profile_pictures['pic']:
        add_profile_picture(profile_pictures['dir'], pp['user'], pp['img'])

    for hp in hair_pictures['pic']:
        add_hair_picture(hair_pictures['dir'], hp['user'], hp['img'])

    for pp in page_pictures['pic']:
        add_page_picture(page_pictures['dir'], pp['user'], pp['img'])

    for treatment in hairdresser_treatments:
        slug = treatment.pop('hairdresser_slug')
        page = Page.objects.get(slug=slug)

        Treatment.objects.get_or_create(
            page=page,
            **treatment
        )[0].save()


if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
