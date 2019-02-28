import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TeamI.settings')
import django
django.setup()
from trimit.models import Page, UserProfile, Review
from django.contrib.auth.models import User


def populate():

    users = [
        {
            "username": "user1",
            "password": "1",
            "type": 0,
        },
        {
            "username": "user2",
            "password": "2",
            "type": 0,
        },
        {
            "username": "user3",
            "password": "3",
            "type": 0,
        },
        {
            "username": "stylist1",
            "password": "1",
            "type": 1,
            "page": 0,
        },
        {
            "username": "stylist2",
            "password": "2",
            "type": 1,
            "page": 1,
        },
        {
            "username": "stylist3",
            "password": "3",
            "type": 1,
            "page": 2,
        },
    ]

    profiles = [
        {
            "user": users[0]["username"],
        },
        {
            "user": users[1]["username"],
        },
        {
            "user": users[2]["username"],
        }
    ]

    hairdresser_pages = [
        {
            "user": users[3]["username"],
            "str": "1 Argyle Str",
            "city": "Glasgow",
            "country": "UK",
        },
        {
            "user": users[4]["username"],
            "str": "5 Bath Str",
            "city": "Glasgow",
            "country": "UK",
        },
        {
            "user": users[5]["username"],
            "str": "50 Great Western Road",
            "city": "Glasgow",
            "country": "UK",
        }
    ]

    reviews = [
        {
            "user": users[0]["username"],
            "page": users[3]["username"],
            "rating": 5.0,
            "comment": "test1",
        },
        {
            "user": users[1]["username"],
            "page": users[4]["username"],
            "rating": 3.5,
            "comment": "test2",
        },
        {
            "user": users[2]["username"],
            "page": users[3]["username"],
            "rating": 4.5,
            "comment": "test3",
        },
        {
            "user": users[0]["username"],
            "page": users[4]["username"],
            "rating": 2.7,
            "comment": "test4",
        },
        {
            "user": users[0]["username"],
            "page": users[5]["username"],
            "rating": 1.5,
            "comment": "test5",
        },
    ]

    def add_user(username, password):
        user = User.objects.get_or_create(username=username, password=password)[0]
        user.save()

    def add_userprofile(username):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.save()

    def add_page(username, street, city, country):
        user = User.objects.get(username=username)
        page = Page.objects.get_or_create(user=user, street_address=street, city=city, country=country)[0]
        page.save()

    def add_review(username, pagename, rating, comment):
        user = User.objects.get(username=username)
        page = Page.objects.get(user=User.objects.get(username=pagename))
        review = Review.objects.get_or_create(page=page, user=user, overall_rating=rating, comment=comment)[0]
        review.save()

    for us in users:
        add_user(us['username'], us['password'])
        if us['type'] == 0:
            add_userprofile(us['username'])
        if us['type'] == 1:
            hairdresser = hairdresser_pages[us['page']]
            u = User.objects.get(username=us['username'])
            add_page(u, hairdresser['str'], hairdresser['city'], hairdresser['country'])

    for rev in reviews:
        add_review(rev['user'], rev['page'], rev['rating'], rev['comment'])

    for u in User.objects.all():
        for p in UserProfile.objects.filter(user=u):
            print("- {0} - UserProfile {1}".format(str(u), str(p)))
        for p in Page.objects.filter(user=u):
            for r in Review.objects.filter(page=p):
                print("- {0} - HairDresserPage {1} - Review {2}".format(str(u), str(p), str(r)))


if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
