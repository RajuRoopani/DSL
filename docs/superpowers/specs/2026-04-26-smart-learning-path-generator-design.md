# Smart Learning Path Generator — Design Spec
**Date:** 2026-04-26  
**Status:** Approved

---

## Overview

A React single-page app that guides users through a 4-step wizard to generate a personalized, week-by-week study roadmap for DSA, Web Development, or AI/ML. After generation, users track their progress through a timeline + task drawer view. The Django backend (already running) serves as the API layer; no new backend framework is introduced.

---

## Scope

**In scope:**
- 4-step wizard: Skill → Level → Time → Goals
- Rule-based roadmap generation from existing Django database content
- Week-by-week roadmap view with timeline (left) + task drawer (right)
- Topic-level progress tracking (checkbox → PATCH API)
- Seed data for DSA, Web Dev, and AI skills with real topics and resources

**Out of scope:**
- Auth UI in React (login/signup stays on existing Django HTML pages)
- Leaderboard, profile, badges in React
- AI-generated roadmaps
- Mobile-specific layout optimization (responsive but not mobile-first)

---

## Architecture

```
repo/
├── smartlearning/               # Django backend (port 8080)
│   ├── roadmap/
│   │   ├── utils.py             # Implement generate_roadmap() — rule-based logic
│   │   └── management/
│   │       └── commands/
│   │           └── seed_skills.py   # Seed DSA, Web Dev, AI content
│   └── api/
│       ├── views.py             # Add generate and progress endpoints
│       └── urls.py              # Wire new routes
└── client/                      # React app (Vite + React 18, port 5173)
    ├── src/
    │   ├── pages/
    │   │   ├── Generator.jsx    # Wizard container (manages step state)
    │   │   └── Roadmap.jsx      # Timeline + drawer container
    │   ├── components/
    │   │   ├── wizard/
    │   │   │   ├── Step1Skill.jsx
    │   │   │   ├── Step2Level.jsx
    │   │   │   ├── Step3Time.jsx
    │   │   │   └── Step4Goals.jsx
    │   │   ├── roadmap/
    │   │   │   ├── WeekTimeline.jsx
    │   │   │   ├── TaskDrawer.jsx
    │   │   │   ├── ProgressBar.jsx
    │   │   │   └── RoadmapHeader.jsx
    │   │   └── ui/
    │   │       ├── Button.jsx
    │   │       ├── Card.jsx
    │   │       └── Badge.jsx
    │   ├── api/
    │   │   └── client.js        # Axios instance — base URL :8080, token from localStorage
    │   ├── App.jsx              # Routes: /generate, /roadmap/:id
    │   └── main.jsx
    ├── package.json
    └── vite.config.js           # Proxy /api → localhost:8080
```

**Communication:** React reads `authToken` from `localStorage`. All requests include `Authorization: Token <authToken>`. The Vite dev proxy forwards `/api/*` to `localhost:8080` to avoid CORS.

**Token handoff:** The Django `login_view` is updated to, after successful login, get-or-create the DRF auth token for the user and redirect to `http://localhost:5173/?token=<token>`. The React `App.jsx` on mount checks for a `?token=` query param, saves it to `localStorage`, and redirects to `/generate`. This means React users always enter via the Django login page.

**On 401:** `client.js` interceptor redirects to `http://localhost:8080/users/login/`.

---

## New Django API Endpoints

### `POST /api/roadmaps/generate`

Generates a week-by-week roadmap for the authenticated user.

**Request:**
```json
{
  "skill_id": 1,
  "level": "beginner",
  "hours_per_week": 10,
  "goal": "interview_prep"
}
```

**Response:**
```json
{
  "id": 42,
  "skill": { "id": 1, "name": "DSA", "icon_emoji": "🧮" },
  "level": "beginner",
  "hours_per_week": 10,
  "goal": "interview_prep",
  "total_weeks": 6,
  "percent_complete": 0,
  "weeks": [
    {
      "week": 1,
      "title": "Arrays & Strings",
      "topics": [
        {
          "id": 7,
          "title": "Array fundamentals",
          "estimated_hours": 1.5,
          "completed": false,
          "resources": [
            { "id": 12, "title": "Arrays Crash Course", "url": "...", "resource_type": "video" }
          ]
        }
      ]
    }
  ]
}
```

**Generation logic** (`roadmap/utils.py`):
1. Fetch all published Topics for the given skill, filtered to the requested difficulty level.
2. Sort by `topic.order`.
3. Group into weeks: accumulate `estimated_hours` per week; start a new week when the running total exceeds `hours_per_week`.
4. Apply `goal` as a resource-ordering hint: `interview_prep` sorts resources with `resource_type='exercise'` first; `portfolio` sorts `resource_type='tutorial'` first; `general` uses default order. Goal does not filter topics — it only reorders resources within each topic.
5. Save a `UserSkillProgress` record (`mastery_level=1`) and return the structured response.

### `PATCH /api/roadmaps/{id}/progress`

Marks a topic complete or incomplete.

**Request:**
```json
{ "topic_id": 7, "completed": true }
```

**Response:**
```json
{ "roadmap_id": 42, "percent_complete": 17 }
```

**Logic:** Toggle `completed` flag on the topic (stored in a new `RoadmapTopicProgress` join table). Recompute `percent_complete = completed_topics / total_topics * 100`. Update `UserSkillProgress.topics_completed` and `mastery_level` accordingly.

### `GET /api/roadmaps/{id}`

Returns the full roadmap (same shape as generate response) with current `completed` state per topic. Used on page reload.

### `GET /api/skills/`

Already exists — returns available skills. The wizard Step 1 fetches this to populate the skill picker.

---

## New Django Model

**`RoadmapTopicProgress`** (in `roadmap/models.py`):
```python
class RoadmapTopicProgress(models.Model):
    user         = ForeignKey(User)
    skill        = ForeignKey(Skill)
    topic        = ForeignKey(Topic)
    completed    = BooleanField(default=False)
    completed_at = DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'skill', 'topic')
```

A `Roadmap` model stores the generation parameters per user+skill:
```python
class Roadmap(models.Model):
    LEVEL_CHOICES = [('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')]
    GOAL_CHOICES  = [('interview_prep','Interview Prep'),('portfolio','Portfolio Project'),('general','General Learning')]

    user           = ForeignKey(User, on_delete=CASCADE)
    skill          = ForeignKey(Skill, on_delete=CASCADE)
    level          = CharField(max_length=20, choices=LEVEL_CHOICES)
    hours_per_week = IntegerField()
    goal           = CharField(max_length=20, choices=GOAL_CHOICES)
    created_at     = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')  # one active roadmap per user per skill
```

**Re-generation:** If a user generates a roadmap for a skill they already have one for, the existing `Roadmap` record and all its `RoadmapTopicProgress` rows are deleted and recreated. Progress resets. The UI warns: "You already have a DSA roadmap. Regenerating will reset your progress."

---

## React Pages & Components

### `Generator.jsx` — `/generate`
- Manages `step` (1–4) and `formData` state.
- Fetches `/api/skills/` on mount for Step 1 options.
- On Step 4 submit: POST `/api/roadmaps/generate` → navigate to `/roadmap/:id`.
- Back/Next buttons; no step is skippable.

### Wizard Steps

| Component | Input type | Options |
|---|---|---|
| `Step1Skill` | Card picker (3 cards) | DSA 🧮, Web Dev 🌐, AI/ML 🤖 |
| `Step2Level` | Card picker (3 cards) | Beginner, Intermediate, Advanced |
| `Step3Time` | Button group | 2 hrs/wk, 5 hrs/wk, 10 hrs/wk, 20 hrs/wk |
| `Step4Goals` | Select dropdown | Interview Prep, Portfolio Project, General Learning |

### `Roadmap.jsx` — `/roadmap/:id`
- Fetches `GET /api/roadmaps/:id` on mount.
- `selectedWeek` state (default: first incomplete week).
- Passes week list to `WeekTimeline`, selected week's topics to `TaskDrawer`.
- On checkbox toggle: optimistic UI update + PATCH `/api/roadmaps/:id/progress`.

### `WeekTimeline`
- Vertical list of week cards.
- Green border + checkmark = complete; purple border = selected/current; muted = locked.
- Click handler updates `selectedWeek` in parent.

### `TaskDrawer`
- Shows week title, estimated hours, topic checkboxes, and resource links.
- Each checkbox fires `onToggle(topicId, completed)` up to `Roadmap.jsx`.
- Resource links open in new tab.

### `ProgressBar`
- Single horizontal bar at top; percentage label on right.
- Animates on update via CSS transition.

---

## Seed Data (`seed_skills` command)

Three skills seeded with full topic + resource trees:

| Skill | Topics | Approx weeks (10 hrs/wk, beginner) |
|---|---|---|
| DSA 🧮 | Arrays, Linked Lists, Stacks/Queues, Trees, Graphs, DP, Sorting, Searching | 8 |
| Web Dev 🌐 | HTML/CSS, JS Fundamentals, React Basics, REST APIs, Node/Express, Databases, Deployment | 7 |
| AI/ML 🤖 | Python for ML, NumPy/Pandas, Linear Regression, Classification, Neural Nets, CNNs, NLP Basics | 7 |

Each topic has 2–4 resources (mix of video, article, interactive).

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Not logged in (no token) | `client.js` interceptor redirects to `/users/login/` |
| `generate` returns 4xx | Wizard shows inline error toast; stays on Step 4 |
| `progress` PATCH fails | Optimistic UI rolled back; checkbox reverts |
| `/roadmap/:id` returns 404 | `Roadmap.jsx` shows "Roadmap not found" with link back to `/generate` |
| Django offline | Generic "Could not connect" banner |

---

## Testing

- Django: unit tests for `generate_roadmap()` logic (week grouping, hours calculation) in `roadmap/tests.py`
- React: component tests for wizard step transitions and `TaskDrawer` checkbox toggle using Vitest + React Testing Library

---

## Out-of-Scope Decisions

- **No Redux / Zustand** — local state is sufficient for this two-page scope.
- **No TypeScript** — plain JSX to keep the build simple; can be added later.
- **No mobile-specific layout** — Tailwind responsive classes used but not the primary target.
- **Token storage** — `localStorage` is acceptable for this project's scope; production would use httpOnly cookies.
