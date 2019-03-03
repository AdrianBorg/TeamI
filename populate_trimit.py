import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TeamI.settings')
import django
django.setup()
from trimit.models import Page, UserProfile, Review, UserHairImage, PageImage
# from trimit.models import EUser as User
from django.contrib.auth.models import User
from django.conf import settings
from django_countries import countries
from django.core.files import File
import os

POPULATE_DIR = os.path.join(settings.STATIC_DIR, 'population')

def populate():

    users = [
        {
            "username": "user1",
            "password": "1",
            "email": "user1@trimit.com",
        },
        {
            "username": "user2",
            "password": "2",
            "email": "user2@trimit.com",
        },
        {
            "username": "user3",
            "password": "3",
            "email": "user3@trimit.com",
        },
        {
            "username": "user4",
            "password": "4",
            "email": "user4@trimit.com",
        },
    ]

    deleting_users = [
        {
            "username": "user4",
        },
    ]

    # profiles = [
    #     {
    #         "user": users[0]["username"],
    #     },
    #     {
    #         "user": users[1]["username"],
    #     },
    #     {
    #         "user": users[2]["username"],
    #     }
    # ]

    stylists = [
        {
            "username": "stylist1",
            "password": "1",
            "email": "stylist1@trimit.com",
        },
        {
            "username": "stylist2",
            "password": "2",
            "email": "stylist2@trimit.com",
        },
        {
            "username": "stylist3",
            "password": "3",
            "email": "stylist3@trimit.com",
        },
        {
            "username": "stylist4",
            "password": "4",
            "email": "stylist4@trimit.com",
        }
    ]

    hairdresser_pages = [
        {
            "str": "1 Argyle Str",
            "city": "Glasgow",
            "country": "GB",
        },
        {
            "str": "5 Bath Str",
            "city": "Glasgow",
            "country": "GB",
        },
        {
            "str": "50 Great Western Road",
            "city": "Glasgow",
            "country": "GB",
        },
        {
            "str": "90 triq il-kbira",
            "city": "Siggiewi",
            "country": "MT",
        },
    ]

    review_pictures_dir = os.path.join(POPULATE_DIR, 'review_pictures')

    reviews = [
        {
            "user": users[0]["username"],
            "page": stylists[0]["username"],
            "rating": 5.0,
            "comment": "test1",
            "img": 'revpic.jpg',
        },
        {
            "user": users[1]["username"],
            "page": stylists[1]["username"],
            "rating": 3.5,
            "comment": "test2",
            "img": None,
        },
        {
            "user": users[2]["username"],
            "page": stylists[0]["username"],
            "rating": 4.5,
            "comment": "test3",
            "img": None,
        },
        {
            "user": users[0]["username"],
            "page": stylists[1]["username"],
            "rating": 2.7,
            "comment": "test4",
            "img": None,
        },
        {
            "user": users[0]["username"],
            "page": stylists[2]["username"],
            "rating": 1.5,
            "comment": "test5",
            "img": None,
        },
        {
            "user": users[3]["username"],
            "page": stylists[2]["username"],
            "rating": 0.6,
            "comment": "deletedtest5",
            "img": None,
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

    def add_user(username, password, email):
        user, created = User.objects.get_or_create(username=username, password=password, email=email)
        if created:
            user.save()

    def add_userprofile(username):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.save()

    def add_page(username, street, city, country):
        user = User.objects.get(username=username)
        print(country)
        for c in list(countries):
            if country.lower() == c[1].lower() or country.lower == c[0].lower:
                cntry = country

        page = Page.objects.get_or_create(user=user, street_address=street, city=city, country=cntry)[0]
        page.save()

    def add_review(username, pagename, rating, comment, img):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        page = Page.objects.get(user=User.objects.get(username=pagename))
        review = Review.objects.get_or_create(page=page, user=user, overall_rating=rating, comment=comment)[0]
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

    for us in users:
        add_user(us['username'], us['password'], us['email'])
        add_userprofile(us['username'])

    i = 0

    for hs in stylists:
        add_user(hs['username'], hs['password'], hs['email'])
        hairdresser = hairdresser_pages[i]
        u = User.objects.get(username=hs['username'])
        add_page(u, hairdresser['str'], hairdresser['city'], hairdresser['country'])
        i += 1

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


if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
