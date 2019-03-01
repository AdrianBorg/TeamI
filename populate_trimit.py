import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TeamI.settings')
import django
django.setup()
from trimit.models import Page, UserProfile, Review
from trimit.models import EUser as User
from django.conf import settings
from django_countries import countries


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

    reviews = [
        {
            "user": users[0]["username"],
            "page": stylists[0]["username"],
            "rating": 5.0,
            "comment": "test1",
        },
        {
            "user": users[1]["username"],
            "page": stylists[1]["username"],
            "rating": 3.5,
            "comment": "test2",
        },
        {
            "user": users[2]["username"],
            "page": stylists[0]["username"],
            "rating": 4.5,
            "comment": "test3",
        },
        {
            "user": users[0]["username"],
            "page": stylists[1]["username"],
            "rating": 2.7,
            "comment": "test4",
        },
        {
            "user": users[0]["username"],
            "page": stylists[2]["username"],
            "rating": 1.5,
            "comment": "test5",
        },
        {
            "user": users[3]["username"],
            "page": stylists[2]["username"],
            "rating": 0.6,
            "comment": "deletedtest5",
        },
    ]

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

    def add_review(username, pagename, rating, comment):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        page = Page.objects.get(user=User.objects.get(username=pagename))
        review = Review.objects.get_or_create(page=page, user=user, overall_rating=rating, comment=comment)[0]
        review.save()

    def delete_user(username):
        user = User.objects.get(username=username)
        user.delete()

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
        add_review(rev['user'], rev['page'], rev['rating'], rev['comment'])

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


if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
