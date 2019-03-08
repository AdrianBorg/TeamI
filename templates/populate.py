import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TeamI.settings')

import django

django.setup()

from trimit.models import Page


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    

    add_hairdresserpage("My Hairdresser Page", "Glasgow")


for m in Page.objects.all():
        print('- {0}:{1}'.format(str(m)))

def add_hairdresserpage(name, location):
    m = Page.objects.get_or_create(name=name, location=location)



if __name__ == '__main__':
    print("Starting Trimit population script...")
    populate()