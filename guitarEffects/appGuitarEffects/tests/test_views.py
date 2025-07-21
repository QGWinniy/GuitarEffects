from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponseRedirect

from appGuitarEffects.models import Song, Group
from appGuitarEffects.forms import SongForm
from appGuitarEffects.views import index, song_detail, group_detail, search_results, form_default


class AppGuitarEffectsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group')
        self.song = Song.objects.create(
            title='Test Song',
            group=self.group,
            effects='Test effects',
            guitar_model='Test guitar',
            amplifier='Test amp',
            description='Test description'
        )

    def test_index_view_get(self):
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Test Song', content)

    def test_index_view_post_default_form(self):
        initial_count = Song.objects.count()
        
        request = self.factory.post('/', {
            'form_type': 'default',
            'title': 'New Song',
            'group': 'New Group',
            'effects': 'New effects',
            'guitar_model': 'New guitar',
            'amplifier': 'New amp',
            'description': 'New description'
        })
        
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, 'messages', messages)

        response = index(request)
        
        self.assertEqual(Song.objects.count(), initial_count + 1)
        
        if response.status_code != 302:
            form = response.context_data.get('form')
            if form:
                print("Form errors:", form.errors)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_song_detail_view(self):
        request = self.factory.get(f'/songs/{self.song.id}/')
        response = song_detail(request, self.song.id)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Test Song', content)

    def test_group_detail_view(self):
        request = self.factory.get(f'/group/{self.group.id}/')
        response = group_detail(request, self.group.id)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Test Group', content)

    def test_search_results_with_query(self):
        request = self.factory.get('/search/?q=Test')
        response = search_results(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Test Song', content)

    def test_search_results_without_query(self):
        request = self.factory.get('/search/')
        response = search_results(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/')

    def test_form_default_valid(self):
        request = self.factory.post('/', {
            'title': 'Another Song',
            'group': 'Another Group',
            'effects': 'Another effects',
            'guitar_model': 'Another guitar',
            'amplifier': 'Another amp',
            'description': 'Another description'
        })
        
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, 'messages', messages)

        response = form_default(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        self.assertTrue(Group.objects.filter(name='Another Group').exists())
        self.assertTrue(Song.objects.filter(title='Another Song').exists())