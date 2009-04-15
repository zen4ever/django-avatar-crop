"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client  
from profiles.models import Profile
from django.core.urlresolvers import reverse
import os.path
from django.conf import settings
from django.http import HttpResponseRedirect

class SimpleTest(TestCase):
    
    fixtures=['users.json']

    def test_avatar_upload_view(self):
        """
        Tests that avatar upload view saves images to the right place 
        """
        c = Client()
        result = c.login(username='andrew', password='andrew')
        self.assertEquals(result, True)
        response = c.get(reverse('profiles_avatar_upload'))
        self.assertEquals(response.status_code, 200)

    def test_image_upload(self):
        """
        Tests that avatar upload view saves images to the right place 
        """
        c = Client()
        f = open(os.path.join(settings.PROJECT_PATH, settings.STATIC_ROOT, 'test/zeratul.jpg'))
        result = c.login(username='andrew', password='andrew')
        self.assertEquals(result, True)
        response = c.post(reverse('profiles_avatar_upload'), {'photo':f})
        self.assertEquals(response.status_code, 302)
        profile = Profile.objects.filter()[0]
        import re
        pre = re.compile(r'^photos/zeratul(_*)\.jpg$')
        are = re.compile(r'^avatars/zeratul(_*)\.jpg$')
        self.failIfEqual(pre.match(profile.photo.name), None)
        self.failIfEqual(are.match(profile.avatar.name), None)
        profile.delete()

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

