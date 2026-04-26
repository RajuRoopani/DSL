SmartLearning - Django project skeleton

This folder contains a skeleton Django project with apps: users, roadmap, progress, dashboard.

Quick start

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start dev server:

```bash
python manage.py migrate
python manage.py runserver
```

Files

- `smartlearning/` - Django project settings
- `users/`, `roadmap/`, `progress/`, `dashboard/` - app skeletons
- `templates/` and `static/` - base templates and assets

API endpoints (examples)

- Obtain token (POST): `/api-token-auth/` with `username` and `password`. Returns `token`.
- Roadmap Skill list (GET): `/roadmap/api/skills/`
- Generate roadmap (GET): `/roadmap/api/generate/<skill_id>/`
- Progress CRUD: `/progress/api/progress/` (authenticated users can POST to create their progress)
- Leaderboard: `/progress/api/leaderboard/`

To load sample data:

```bash
python manage.py loaddata roadmap/fixtures/skills.json roadmap/fixtures/topics.json roadmap/fixtures/resources.json
```

CI

This repository includes a GitHub Actions workflow that runs the Django test suite on push and PRs: `.github/workflows/python-app.yml`.
