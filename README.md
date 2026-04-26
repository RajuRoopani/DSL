# SmartLearning 🎓

A full-stack learning management platform with a Django REST API backend and a React/Vite frontend that generates personalized learning roadmaps.

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

### Backend
- **Django 4.2** + **Django REST Framework 3.17** — API server on port 8080
- **SQLite** (dev) — switchable to PostgreSQL/MySQL
- **DRF Token Auth** — token issued on login, forwarded to React frontend

### Frontend
- **React 18** + **Vite 5** — SPA on port 5173
- **React Router 6** — client-side routing
- **Axios** — HTTP client with auth interceptor
- **Vitest** + **React Testing Library** — unit tests

## 📋 Project Structure

```
DSL/
├── smartlearning/               # Django project root
│   ├── smartlearning/           # Project settings & URLs
│   ├── users/                   # Auth: signup, login, profile
│   ├── roadmap/                 # Skills, Topics, Resources, Roadmap models
│   │   ├── models.py            # Skill, Topic, Resource, Roadmap, RoadmapTopicProgress
│   │   ├── utils.py             # Rule-based roadmap generation logic
│   │   └── management/commands/seed_skills.py  # Seed DSA/Web/AI skills
│   ├── progress/                # XP progress tracking
│   ├── dashboard/               # Dashboard & leaderboard views
│   ├── activity/                # Activity logging & statistics
│   ├── api/                     # Unified REST API (views, serializers, URLs)
│   └── templates/               # Django HTML templates
└── client/                      # React/Vite frontend
    ├── src/
    │   ├── api/client.js        # Axios instance with token auth interceptor
    │   ├── pages/
    │   │   ├── Generator.jsx    # 4-step wizard orchestrator
    │   │   └── Roadmap.jsx      # Roadmap view with progress tracking
    │   ├── components/
    │   │   ├── wizard/          # Step1Skill, Step2Level, Step3Time, Step4Goals
    │   │   └── roadmap/         # WeekTimeline, TaskDrawer, ProgressBar, RoadmapHeader
    │   └── App.jsx              # TokenCapture + React Router routes
    ├── vite.config.js           # Proxy /api → localhost:8080
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- pip

### Backend Setup

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

5. **Seed skills and topics**
```bash
python manage.py seed_skills
```
This seeds DSA, Web Development, and AI/ML skills with topics and resources. Safe to re-run (uses `update_or_create`).

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start Django on port 8080**
```bash
python manage.py runserver 8080
```

### Frontend Setup

In a second terminal:

```bash
cd DSL/client
npm install
npm run dev
```

The React app starts at http://localhost:5173.

### Using the App

1. Visit http://localhost:8080 and sign up or log in
2. On successful login, Django issues a token and redirects to http://localhost:5173/?token=...
3. The React app captures the token and opens the **Generate Roadmap** wizard
4. Complete the 4-step wizard → your personalized roadmap is created
5. Check off topics as you complete them
6. Return to http://localhost:8080/dashboard/ to see your enrolled courses and progress

## 🔑 Authentication Flow

Login at `http://localhost:8080/users/login/` → Django authenticates the user, creates a DRF Token, and redirects to `http://localhost:5173/?token=<key>`. The React `TokenCapture` component saves the token to `localStorage` and all subsequent API calls include `Authorization: Token <key>`.

## 📡 API Endpoints

### Authentication

```
POST   /api-token-auth/                    # Get token by username/password
```

### Skills
```
GET    /api/skills/                        # List all skills
GET    /api/skills/{id}/                   # Skill details with topics
GET    /api/topics/                        # Topics (filterable by skill)
GET    /api/resources/                     # Resources (filterable by topic)
```

### Roadmaps (Token required)
```
POST   /api/roadmaps/generate              # Generate a personalized roadmap
       Body: { skill_id, level, hours_per_week, goal }
       level: beginner | intermediate | advanced
       goal: interview_prep | portfolio | general

GET    /api/roadmaps/{id}                  # Get roadmap with week-grouped topics

PATCH  /api/roadmaps/{id}/progress         # Mark a topic complete/incomplete
       Body: { topic_id, completed }
```

### Users & Stats
```
GET    /api/profiles/                      # List profiles
GET    /api/user-badges/                   # My badges
GET    /api/dashboard-stats/               # Comprehensive dashboard data
GET    /api/leaderboard/                   # Global leaderboard
GET    /api/skill-progress/                # My skill progress
```

### Query Parameters
- `search=<term>` — full-text search
- `limit=<n>` / `offset=<n>` — pagination
- `ordering=<field>` — sort (`-field` for descending)
- `difficulty=beginner|intermediate|advanced` — filter by difficulty
- `category=<name>` — filter by category

## 📊 Models Overview

### Roadmap App
- **Skill** — learning skill with difficulty, category, prerequisites, popularity score
- **Topic** — topic within a skill with estimated hours and difficulty level
- **Resource** — learning materials (video, article, course, exercise, tutorial)
- **Roadmap** — user's active roadmap for a skill (one per user per skill)
- **RoadmapTopicProgress** — completion state for each topic in a roadmap

### Users App
- **Profile** — enhanced user profile with XP, streak tracking, social links
- **Badge** — achievement badges with unlock criteria
- **UserBadge** — earned badges per user

### Activity App
- **ActivityLog** — audit trail of user actions
- **UserStatistics** — aggregated learning statistics

## 🧪 Testing

### Django tests
```bash
cd smartlearning
python manage.py test
```

### React tests
```bash
cd client
npm test
```

Run with coverage:

```bash
# Django
coverage run --source='.' manage.py test
coverage report

# React
npm run test -- --coverage
```

## 🎨 UI Pages

### Django (port 8080)
- **Home** (`/`) — welcome page
- **Login** (`/users/login/`) — issues token and redirects to React
- **Sign Up** (`/users/signup/`) — new account registration
- **Dashboard** (`/dashboard/`) — skill cards with live progress
- **Leaderboard** (`/dashboard/leaderboard/`) — global rankings
- **Profile** (`/users/profile/`) — XP display and stats
- **Admin Panel** (`/admin/`) — Django admin

### React (port 5173)
- **Generate Roadmap** (`/generate`) — 4-step wizard
- **Roadmap View** (`/roadmap/:id`) — timeline + task drawer with progress

## 🔧 Configuration

### Django settings (smartlearning/settings.py)
```python
DEBUG = True              # Set to False in production
ALLOWED_HOSTS = ['*']     # Configure for production
PORT = 8080               # Run with: python manage.py runserver 8080

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
```

### Vite proxy (client/vite.config.js)
All `/api/*` requests from the React dev server are proxied to `http://localhost:8080` to avoid CORS issues.

## 🚀 Deployment

### Django (Gunicorn + Nginx)

```bash
cd smartlearning
pip install gunicorn
python manage.py collectstatic --noinput
gunicorn smartlearning.wsgi:application --bind 0.0.0.0:8080
```

Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/smartlearning/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### React (production build)

```bash
cd client
npm run build          # outputs to client/dist/
```

Serve `client/dist/` with Nginx or any static file host.

## 🐛 Troubleshooting

### No courses on the dashboard
Run `python manage.py seed_skills` to populate skills and topics.

### Login doesn't redirect to React
Make sure both servers are running — Django on port 8080 and React dev server on port 5173.

### Migration errors
```bash
python manage.py migrate --fake-initial
# or reset in dev:
rm db.sqlite3
python manage.py migrate
python manage.py seed_skills
python manage.py createsuperuser
```

### React API calls return 401
Token not in localStorage. Log in again via http://localhost:8080/users/login/ to get a fresh token redirect.

### PostCSS / Tailwind errors in React build
The `client/postcss.config.js` file (empty export) overrides any parent directory PostCSS config. Do not remove it.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License — see the LICENSE file for details.

## 👤 Author

Smart Learning Team

## 📞 Support

- 🐛 GitHub Issues: https://github.com/shiva676466/DSL/issues
- 💬 Discussions: https://github.com/shiva676466/DSL/discussions

---

**Happy Learning! 🚀**
