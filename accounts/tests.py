from accounts.models import UserProfile
from testing.testcases import TestCase


# Create your tests here.
class UserProfileTests(TestCase):

    def setUp(self):
        super(UserProfileTests, self).setUp()

    def test_profile_property(self):
        linghu = self.create_user('linghu')
        self.assertEqual(UserProfile.objects.count(), 0)
        p = linghu.profile
        self.assertEqual(isinstance(p, UserProfile), True)
        self.assertEqual(UserProfile.objects.count(), 1)