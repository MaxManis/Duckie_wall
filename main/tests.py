from django.test import TestCase

# Create your tests here.
from main.models import Posts
from django.contrib.auth.models import User


class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    # def test_content_max_length(self):
    #     users = User.objects.all()
    #     for user in users:
    #         user_id = user.id
    #         content = Posts.objects.filter(user=user_id)
    #         for i in content:
    #             length1 = i._meta.get_field('content').max_length
    #             self.assertEquals(length1, 10)

    def test_content_max_length(self):
        content = Posts.objects.filter(user=1)
        for i in content:
            length1 = i._meta.get_field('content').max_length
            self.assertEquals(length1, 10)

    # def test_content_label(self):
    #     users = User.objects.all()
    #     for user in users:
    #         user_id = user.id
    #         content = Posts.objects.filter(user=user_id)
    #         for i in content:
    #             field_label = i._meta.get_field('content').verbose_name
    #             self.assertEquals(field_label, 'Содержание22')
