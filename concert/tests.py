from django.test import TestCase
from django.contrib.auth.models import User
from .models import Concert, ConcertAttending
class ConcertFlowTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('fan',password='test-only-password')
        self.concert=Concert.objects.create(concert_name='Test show',duration=2,city='London')
    def test_guest_cannot_rsvp(self):
        self.assertEqual(self.client.post('/concert_attendee/',{'concert_id':self.concert.pk,'attendee_choice':'Attending'}).status_code,302)
        self.assertEqual(ConcertAttending.objects.count(),0)
    def test_login_and_update_rsvp(self):
        self.assertTrue(self.client.login(username='fan',password='test-only-password'))
        for choice in ['Attending','Not Attending']:
            response=self.client.post('/concert_attendee/',{'concert_id':self.concert.pk,'attendee_choice':choice})
            self.assertEqual(response.status_code,302)
            self.assertEqual(ConcertAttending.objects.get().attending,choice)
        self.assertEqual(ConcertAttending.objects.count(),1)
    def test_invalid_rsvp(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.post('/concert_attendee/',{'concert_id':self.concert.pk,'attendee_choice':'unexpected'}).status_code,400)
        self.assertEqual(ConcertAttending.objects.count(),0)
