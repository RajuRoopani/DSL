from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import Profile, Badge, UserBadge
from roadmap.models import Skill, Topic, Resource, UserSkillProgress
from activity.models import ActivityLog, UserStatistics


class ProfileModelTest(TestCase):
    """Test Profile model and streak logic."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.profile = Profile.objects.get(user=self.user)
    
    def test_profile_creation(self):
        """Test profile is created on user signup."""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.total_xp, 0)
        self.assertEqual(self.profile.current_streak, 0)
    
    def test_add_xp(self):
        """Test adding XP."""
        self.profile.add_xp(50)
        self.assertEqual(self.profile.total_xp, 50)
    
    def test_update_streak(self):
        """Test streak tracking."""
        self.profile.update_streak()
        self.assertEqual(self.profile.current_streak, 1)
        
        # Add 50 XP and update
        self.profile.add_xp(50)
        self.assertEqual(self.profile.current_streak, 1)


class SkillModelTest(TestCase):
    """Test Skill model."""
    
    def setUp(self):
        self.skill1 = Skill.objects.create(
            name='Python',
            category='Programming',
            difficulty='beginner',
            icon_emoji='🐍'
        )
        self.skill2 = Skill.objects.create(
            name='Django',
            category='Framework',
            difficulty='intermediate',
            icon_emoji='🔧',
        )
        # Django depends on Python
        self.skill2.prerequisites.add(self.skill1)
    
    def test_skill_creation(self):
        """Test skill creation."""
        self.assertEqual(self.skill1.name, 'Python')
        self.assertEqual(self.skill1.difficulty, 'beginner')
    
    def test_prerequisites(self):
        """Test prerequisites relationships."""
        self.assertIn(self.skill1, self.skill2.prerequisites.all())


class SkillProgressTest(TestCase):
    """Test UserSkillProgress."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.skill = Skill.objects.create(name='Python', category='Programming')
        self.progress = UserSkillProgress.objects.create(
            user=self.user,
            skill=self.skill,
            mastery_level=1,
            xp_earned=50
        )
    
    def test_progress_creation(self):
        """Test skill progress tracking."""
        self.assertEqual(self.progress.xp_earned, 50)
        self.assertEqual(self.progress.mastery_level, 1)


class ProfileAPITest(APITestCase):
    """Test Profile API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.profile = self.user.profile
        self.profile.total_xp = 100
        self.profile.public_profile = True
        self.profile.save()
        
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
    
    def test_list_public_profiles(self):
        """Test listing public profiles."""
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_retrieve_profile(self):
        """Test retrieving a profile."""
        response = self.client.get(f'/api/profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_xp'], 100)


class SkillAPITest(APITestCase):
    """Test Skill API endpoints."""
    
    def setUp(self):
        self.skill = Skill.objects.create(
            name='Python',
            category='Programming',
            difficulty='beginner',
            popularity_score=9.5
        )
        Skill.objects.create(
            name='JavaScript',
            category='Web',
            difficulty='beginner',
            popularity_score=9.0
        )
    
    def test_list_skills(self):
        """Test listing skills."""
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)
    
    def test_filter_by_difficulty(self):
        """Test filtering skills by difficulty."""
        response = self.client.get('/api/skills/?difficulty=beginner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for skill in response.data['results']:
            self.assertEqual(skill['difficulty'], 'beginner')
    
    def test_search_skills(self):
        """Test searching skills."""
        response = self.client.get('/api/skills/?search=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Python')


class BadgeAPITest(APITestCase):
    """Test Badge API."""
    
    def setUp(self):
        self.badge = Badge.objects.create(
            name='First Steps',
            description='Earned your first 50 XP',
            icon_emoji='🌟',
            badge_type='xp',
            xp_threshold=50
        )
    
    def test_list_badges(self):
        """Test listing available badges."""
        response = self.client.get('/api/badges/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'First Steps')


class LeaderboardAPITest(APITestCase):
    """Test leaderboard endpoint."""
    
    def setUp(self):
        # Create users with different XP
        for i, xp in enumerate([100, 50, 75]):
            user = User.objects.create_user(f'user{i}', f'user{i}@test.com', 'pass')
            profile = user.profile
            profile.total_xp = xp
            profile.public_profile = True
            profile.save()
    
    def test_leaderboard(self):
        """Test leaderboard returns ranked users."""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by XP descending
        self.assertEqual(response.data[0]['total_xp'], 100)
        self.assertEqual(response.data[1]['total_xp'], 75)
        self.assertEqual(response.data[2]['total_xp'], 50)


class RecommendationsAPITest(APITestCase):
    """Test recommendations endpoint."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.token = Token.objects.create(user=self.user)
        
        # Create skills
        for i in range(5):
            Skill.objects.create(
                name=f'Skill {i}',
                category='Test',
                popularity_score=float(10 - i)
            )
    
    def test_recommended_skills(self):
        """Test recommendations for authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/recommended-skills/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['recommended_skills']), 0)


class DashboardStatsAPITest(APITestCase):
    """Test dashboard stats endpoint."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.token = Token.objects.create(user=self.user)
    
    def test_dashboard_stats(self):
        """Test comprehensive dashboard stats."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/dashboard-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile', response.data)
        self.assertIn('statistics', response.data)
        self.assertIn('current_skills', response.data)
        self.assertIn('recent_activity', response.data)
