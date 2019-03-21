from django.test import TestCase
from trimit.models import Category

# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should result True for categories
        where views are zero or positive

        """
        cat = Category(name='test', views = -1,likes=0)
        cat.save()
        self.assertEqual((cat.view > 0), True)