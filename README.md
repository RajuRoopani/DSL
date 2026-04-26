# SmartLearning 🎓

A comprehensive, full-featured learning management and skill-tracking platform built with Django and modern web technologies.

## ✨ Features

### Core Features
- **User Authentication**: Sign up, login, and profile management with Django's auth system
- **Skill Learning Paths**: Curated learning roadmaps with topics and resources
- **Progress Tracking**: Track XP (experience points), skills learned, and learning streaks
- **Leaderboard**: Global ranking system with user statistics and badges
- **Achievements**: Earn badges for milestones and learning streaks
- **Activity Logging**: Comprehensive audit trail of user actions

### Advanced Backend
- **Enhanced Profiles**: Bio, avatar, social links, learning goals, and streak tracking
- **Skill System**: Prerequisites, difficulty levels, categories, and recommendations
- **User Statistics**: Comprehensive stats with rank, percentile, and learning metrics
- **REST API**: Complete API with pagination, filtering, search, and token auth
- **Admin Dashboard**: Fully configured Django admin with rich inline editing

### Beautiful UI
- **Modern Design**: Bootstrap 5 with custom gradients, animations, and shadows
- **Responsive**: Mobile-first design that works on all devices
- **Interactive Charts**: Chart.js leaderboard visualization
- **AJAX Interactions**: Real-time XP updates and profile management

## 🛠️ Tech Stack

- **Backend**: Django 6.0.4, Django REST Framework 3.17.1
- **Frontend**: HTML5, Bootstrap 5, JavaScript (ES6+), Chart.js
- **Database**: SQLite (dev), easily switchable to PostgreSQL/MySQL
- **Authentication**: Django auth + Token auth via DRF
- **Testing**: Django TestCase + DRF APITestCase

## 📋 Project Structure

```
smartlearning/
├── smartlearning/           # Project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI config
├── users/                  # User management app
│   ├── models.py          # Profile, Badge, UserBadge models
│   ├── views.py           # Auth views (signup, profile)
│   ├── serializers.py     # User serializers
│   └── templates/         # Login, signup, profile pages
├── roadmap/               # Learning paths app
│   ├── models.py          # Skill, Topic, Resource, UserSkillProgress
│   ├── views.py           # Skill/topic viewsets
│   ├── serializers.py     # DRF serializers
│   └── templates/         # Roadmap generator
├── progress/              # Progress tracking app
│   ├── models.py          # Progress model
│   ├── views.py           # Progress API endpoints
│   └── serializers.py     # Progress serializers
├── dashboard/             # Analytics & leaderboard
│   ├── views.py           # Dashboard views
│   └── templates/         # Dashboard, leaderboard pages
├── activity/              # Activity logging
│   ├── models.py          # ActivityLog, UserStatistics
│   └── admin.py           # Admin interface
├── api/                   # Unified API
│   ├── views.py           # Comprehensive API viewsets
│   ├── serializers.py     # All serializers
│   ├── urls.py            # API routing
│   ├── tests.py           # API tests
│   └── admin.py           # Admin configs
├── static/                # Static files
│   ├── css/style.css      # Custom styling
│   └── js/                # Client-side JS
└── templates/             # Base templates
    ├── base.html          # Main template
    ├── home.html          # Homepage
    └── includes/          # Navbar, footer
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/shiva676466/DSL.git
cd DSL/smartlearning
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
# Username: admin
# Password: (your secure password)
```

6. **Load demo data (optional)**
```bash
python manage.py loaddata smartlearning/roadmap/fixtures/skills.json
python manage.py loaddata smartlearning/roadmap/fixtures/topics.json
python manage.py loaddata smartlearning/roadmap/fixtures/resources.json
```

7. **Start development server**
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## 🔐 Demo Accounts

If you loaded demo data, you can log in with:

- **alice** / **password** (100 XP)
- **bob** / **password** (80 XP)
- **carol** / **password** (60 XP)

Or create your own account via Sign Up.

## 📡 API Endpoints

### Authentication
```
POST   /api-token-auth/              # Get token
```

### Users & Profiles
```
GET    /api/profiles/                # List profiles
GET    /api/profiles/{id}/           # Get profile
GET    /api/user-badges/             # My badges
GET    /api/badges/                  # Available badges
```

### Skills & Learning
```
GET    /api/skills/                  # List skills (filterable, searchable)
GET    /api/skills/{id}/             # Skill details with topics
GET    /api/topics/                  # Topics (filterable by skill)
GET    /api/resources/               # Resources (filterable by topic)
GET    /api/skill-progress/          # My skill progress
POST   /api/skill-progress/          # Track skill progress
```

### Activity & Stats
```
GET    /api/activity/                # My activity logs
GET    /api/statistics/              # User statistics
GET    /api/dashboard-stats/         # Comprehensive dashboard data
GET    /api/leaderboard/             # Global leaderboard
GET    /api/recommended-skills/      # Personalized recommendations
GET    /api/skill-categories/        # Available categories
```

### Query Parameters
- `search=<term>` - Search in results
- `limit=<n>` - Pagination limit (default: 20)
- `offset=<n>` - Pagination offset
- `ordering=<field>` - Order by field (use `-field` for desc)
- `difficulty=beginner|intermediate|advanced|expert` - Filter by difficulty
- `category=<name>` - Filter by category

## 🧪 Testing

Run the full test suite:
```bash
python manage.py test
```

Run specific test module:
```bash
python manage.py test api.tests.ProfileAPITest
```

Run with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🎨 UI Pages

### Public Pages
- **Home** (`/`) - Welcome page with feature highlights
- **Login** (`/accounts/login/`) - User login form
- **Sign Up** (`/users/signup/`) - New account registration

### Authenticated Pages
- **Profile** (`/users/profile/`) - User profile with XP display and add XP button
- **Roadmap Generator** (`/roadmap/generate/`) - Generate learning paths
- **Leaderboard** (`/dashboard/leaderboard/`) - Global rankings with Chart.js visualization
- **Dashboard** (`/dashboard/`) - User statistics overview

### Admin
- **Admin Panel** (`/admin/`) - Django admin with all models

## 📊 Models Overview

### Users App
- **Profile**: Enhanced user profile with streak tracking, social links, learning stats
- **Badge**: Achievement badges with unlock criteria
- **UserBadge**: Track earned badges per user

### Roadmap App
- **Skill**: Learning skills with difficulty, category, prerequisites
- **Topic**: Topics within skills with learning objectives
- **Resource**: Learning materials (video, article, course, etc.)
- **UserSkillProgress**: Track user progress on individual skills

### Progress App
- **Progress**: XP entries for users

### Activity App
- **ActivityLog**: Audit trail of user actions
- **UserStatistics**: Aggregated user learning statistics

## 🔧 Configuration

### Settings (smartlearning/settings.py)

Key configurations:
```python
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['*']  # Configure for production
SECRET_KEY = 'change-me'  # Use environment variable in production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

## 📚 API Usage Examples

### Get User Profile
```bash
curl http://127.0.0.1:8000/api/profiles/1/
```

### Search Skills
```bash
curl "http://127.0.0.1:8000/api/skills/?search=Python&difficulty=beginner"
```

### Add XP (Authenticated)
```bash
curl -X POST http://127.0.0.1:8000/progress/api/progress/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"xp": 50}'
```

### Get Dashboard Stats (Authenticated)
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/dashboard-stats/
```

## 🚀 Deployment

### Using Gunicorn + Nginx (Production)

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

3. **Run with Gunicorn**
```bash
gunicorn smartlearning.wsgi:application --bind 0.0.0.0:8000
```

4. **Configure Nginx** (reverse proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/smartlearning/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "smartlearning.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t smartlearning .
docker run -p 8000:8000 smartlearning
```

## 📖 Documentation

### API Documentation
Full API documentation with request/response examples is available in the code:
- See `api/serializers.py` for field documentation
- See `api/views.py` for endpoint documentation
- Test endpoints in `api/tests.py`

### Model Documentation
Comprehensive model documentation available in:
- `users/models.py` - Profile, Badge models
- `roadmap/models.py` - Skill, Topic, Resource models
- `activity/models.py` - ActivityLog, UserStatistics

## 🐛 Troubleshooting

### Migration Errors
```bash
# Reset migrations (dev only)
python manage.py migrate --fake users zero
python manage.py migrate
```

### Import Errors
```bash
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Delete and recreate database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Smart Learning Team

## 🙏 Acknowledgments

- Django community
- Django REST Framework
- Bootstrap team
- Chart.js team

## 📞 Support

For issues and questions:
- 📧 Email: support@smartlearning.dev
- 🐛 GitHub Issues: https://github.com/shiva676466/DSL/issues
- 💬 Discussions: https://github.com/shiva676466/DSL/discussions

---

**Happy Learning! 🚀**
