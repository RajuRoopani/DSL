from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Skill
from .models import Topic, Resource


class SkillAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Skill.objects.create(name='Python')

    def test_list_skills(self):
        url = reverse('skill-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 1)



class RoadmapAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        s = Skill.objects.create(name='Python')
        t = Topic.objects.create(skill=s, title='Basics', description='Intro')
        Resource.objects.create(topic=t, title='Tutorial', url='https://example.com')

    def test_generate_roadmap(self):
        skill = Skill.objects.first()
        url = reverse('api-generate', args=[skill.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('topics', resp.data)

# *** End Patch