from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Skill, Topic, Resource, Roadmap, RoadmapTopicProgress
from .utils import generate_roadmap, build_roadmap_response


class GenerateRoadmapTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='pass')
        self.skill = Skill.objects.create(name='DSA', icon_emoji='🧮', category='cs')
        Topic.objects.create(skill=self.skill, title='Arrays', difficulty='beginner',
                             estimated_hours=2.0, order=1, status='published')
        Topic.objects.create(skill=self.skill, title='Linked Lists', difficulty='beginner',
                             estimated_hours=3.0, order=2, status='published')
        Topic.objects.create(skill=self.skill, title='Trees', difficulty='intermediate',
                             estimated_hours=4.0, order=3, status='published')

    def test_groups_topics_into_weeks_by_hours(self):
        # 2hrs + 3hrs = 5hrs; with 4hrs/week: Arrays alone in week 1, Linked Lists in week 2
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 4, 'general')
        self.assertEqual(len(result['weeks']), 2)
        self.assertEqual(result['weeks'][0]['topics'][0]['title'], 'Arrays')
        self.assertEqual(result['weeks'][1]['topics'][0]['title'], 'Linked Lists')

    def test_single_topic_that_exceeds_week_still_gets_its_own_week(self):
        # Trees alone (4hrs) with 3hrs/week — should still appear as its own week
        result = generate_roadmap(self.user, self.skill.id, 'intermediate', 3, 'general')
        all_titles = [t['title'] for w in result['weeks'] for t in w['topics']]
        self.assertIn('Trees', all_titles)

    def test_beginner_level_excludes_intermediate_topics(self):
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'general')
        all_titles = [t['title'] for w in result['weeks'] for t in w['topics']]
        self.assertNotIn('Trees', all_titles)

    def test_intermediate_level_includes_beginner_and_intermediate(self):
        result = generate_roadmap(self.user, self.skill.id, 'intermediate', 10, 'general')
        all_titles = [t['title'] for w in result['weeks'] for t in w['topics']]
        self.assertIn('Arrays', all_titles)
        self.assertIn('Trees', all_titles)

    def test_advanced_level_includes_all_topics(self):
        result = generate_roadmap(self.user, self.skill.id, 'advanced', 10, 'general')
        all_titles = [t['title'] for w in result['weeks'] for t in w['topics']]
        self.assertIn('Arrays', all_titles)
        self.assertIn('Trees', all_titles)

    def test_creates_roadmap_record_in_db(self):
        generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'general')
        self.assertTrue(Roadmap.objects.filter(user=self.user, skill=self.skill).exists())

    def test_regenerating_deletes_old_roadmap_and_resets_progress(self):
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'general')
        old_id = result['id']
        result2 = generate_roadmap(self.user, self.skill.id, 'intermediate', 10, 'general')
        self.assertFalse(Roadmap.objects.filter(id=old_id).exists())
        self.assertNotEqual(result2['id'], old_id)

    def test_returns_none_for_unknown_skill(self):
        result = generate_roadmap(self.user, 99999, 'beginner', 10, 'general')
        self.assertIsNone(result)

    def test_percent_complete_is_zero_on_generation(self):
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'general')
        self.assertEqual(result['percent_complete'], 0)

    def test_response_shape(self):
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'general')
        self.assertIn('id', result)
        self.assertIn('skill', result)
        self.assertIn('weeks', result)
        self.assertIn('total_weeks', result)
        self.assertIn('percent_complete', result)
        self.assertEqual(result['skill']['name'], 'DSA')

    def test_interview_prep_goal_sorts_exercise_resources_first(self):
        topic = Topic.objects.get(title='Arrays')
        Resource.objects.create(topic=topic, title='Article', resource_type='article', order=1)
        Resource.objects.create(topic=topic, title='Practice Set', resource_type='exercise', order=2)
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'interview_prep')
        resources = result['weeks'][0]['topics'][0]['resources']
        self.assertEqual(resources[0]['resource_type'], 'exercise')

    def test_portfolio_goal_sorts_tutorial_resources_first(self):
        topic = Topic.objects.get(title='Arrays')
        Resource.objects.create(topic=topic, title='Article', resource_type='article', order=1)
        Resource.objects.create(topic=topic, title='Build Tutorial', resource_type='tutorial', order=2)
        result = generate_roadmap(self.user, self.skill.id, 'beginner', 10, 'portfolio')
        resources = result['weeks'][0]['topics'][0]['resources']
        self.assertEqual(resources[0]['resource_type'], 'tutorial')


class RoadmapAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apiuser', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.skill = Skill.objects.create(name='WebDev', icon_emoji='🌐', category='web')
        self.topic = Topic.objects.create(
            skill=self.skill, title='HTML', difficulty='beginner',
            estimated_hours=2.0, order=1, status='published'
        )

    def test_generate_returns_200_with_weeks(self):
        resp = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('weeks', resp.data)
        self.assertIn('id', resp.data)

    def test_generate_requires_authentication(self):
        self.client.credentials()
        resp = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        self.assertEqual(resp.status_code, 401)

    def test_generate_returns_404_for_unknown_skill(self):
        resp = self.client.post('/api/roadmaps/generate', {
            'skill_id': 99999, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        self.assertEqual(resp.status_code, 404)

    def test_generate_returns_400_for_invalid_level(self):
        resp = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'expert',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_get_roadmap_returns_same_shape(self):
        gen = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        roadmap_id = gen.data['id']
        resp = self.client.get(f'/api/roadmaps/{roadmap_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], roadmap_id)
        self.assertIn('weeks', resp.data)

    def test_get_roadmap_returns_404_for_other_users_roadmap(self):
        gen = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        roadmap_id = gen.data['id']
        other = User.objects.create_user('other', password='pass')
        other_token = Token.objects.create(user=other)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        resp = self.client.get(f'/api/roadmaps/{roadmap_id}')
        self.assertEqual(resp.status_code, 404)

    def test_progress_marks_topic_complete(self):
        gen = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        roadmap_id = gen.data['id']
        resp = self.client.patch(f'/api/roadmaps/{roadmap_id}/progress',
                                  {'topic_id': self.topic.id, 'completed': True}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['percent_complete'], 100)
        self.assertEqual(resp.data['roadmap_id'], roadmap_id)

    def test_progress_marks_topic_incomplete(self):
        gen = self.client.post('/api/roadmaps/generate', {
            'skill_id': self.skill.id, 'level': 'beginner',
            'hours_per_week': 10, 'goal': 'general'
        }, format='json')
        roadmap_id = gen.data['id']
        roadmap = Roadmap.objects.get(id=roadmap_id)
        RoadmapTopicProgress.objects.create(roadmap=roadmap, topic=self.topic, completed=True)
        resp = self.client.patch(f'/api/roadmaps/{roadmap_id}/progress',
                                  {'topic_id': self.topic.id, 'completed': False}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['percent_complete'], 0)
