from .models import Skill, Topic, Roadmap, RoadmapTopicProgress


def generate_roadmap(user, skill_id, level, hours_per_week, goal):
    """
    Generate (or regenerate) a roadmap for user+skill.
    Deletes any existing roadmap for this user+skill first.
    Returns the roadmap response dict, or None if skill not found.
    """
    try:
        skill = Skill.objects.get(id=skill_id)
    except Skill.DoesNotExist:
        return None

    Roadmap.objects.filter(user=user, skill=skill).delete()

    roadmap = Roadmap.objects.create(
        user=user,
        skill=skill,
        level=level,
        hours_per_week=hours_per_week,
        goal=goal,
    )
    return build_roadmap_response(roadmap)


def build_roadmap_response(roadmap):
    """Build the full roadmap dict with current completion state."""
    topics = _fetch_topics_for_level(roadmap.skill, roadmap.level)
    completed_ids = set(
        RoadmapTopicProgress.objects.filter(
            roadmap=roadmap, completed=True
        ).values_list('topic_id', flat=True)
    )

    weeks = _group_into_weeks(topics, roadmap.hours_per_week, roadmap.goal, completed_ids)
    total = sum(len(w['topics']) for w in weeks)
    done = sum(1 for w in weeks for t in w['topics'] if t['completed'])
    percent = round(done / total * 100) if total > 0 else 0

    return {
        'id': roadmap.id,
        'skill': {
            'id': roadmap.skill.id,
            'name': roadmap.skill.name,
            'icon_emoji': roadmap.skill.icon_emoji,
        },
        'level': roadmap.level,
        'hours_per_week': roadmap.hours_per_week,
        'goal': roadmap.goal,
        'total_weeks': len(weeks),
        'percent_complete': percent,
        'weeks': weeks,
    }


def _fetch_topics_for_level(skill, level):
    qs = Topic.objects.filter(skill=skill, status='published')
    if level == 'beginner':
        qs = qs.filter(difficulty='beginner')
    elif level == 'intermediate':
        qs = qs.filter(difficulty__in=['beginner', 'intermediate'])
    # advanced: no difficulty filter — include all
    return qs.order_by('order').prefetch_related('resources')


def _group_into_weeks(topics, hours_per_week, goal, completed_ids):
    weeks = []
    current = []
    current_hours = 0.0
    week_num = 1

    for topic in topics:
        topic_dict = _topic_to_dict(topic, goal, completed_ids)
        # Start a new week if adding this topic would exceed the weekly limit
        # (but never leave a week empty — always add at least one topic per week)
        if current_hours + topic.estimated_hours > hours_per_week and current:
            weeks.append({
                'week': week_num,
                'title': current[0]['title'],
                'topics': current,
            })
            week_num += 1
            current = []
            current_hours = 0.0
        current.append(topic_dict)
        current_hours += topic.estimated_hours

    if current:
        weeks.append({
            'week': week_num,
            'title': current[0]['title'],
            'topics': current,
        })

    return weeks


def _topic_to_dict(topic, goal, completed_ids):
    resources = list(
        topic.resources.all().values('id', 'title', 'url', 'resource_type', 'order')
    )
    resources = _sort_resources_for_goal(resources, goal)
    for r in resources:
        r.pop('order', None)

    return {
        'id': topic.id,
        'title': topic.title,
        'estimated_hours': topic.estimated_hours,
        'completed': topic.id in completed_ids,
        'resources': resources,
    }


def _sort_resources_for_goal(resources, goal):
    if goal == 'interview_prep':
        return sorted(resources, key=lambda r: (0 if r['resource_type'] == 'exercise' else 1, r['order']))
    if goal == 'portfolio':
        return sorted(resources, key=lambda r: (0 if r['resource_type'] == 'tutorial' else 1, r['order']))
    return sorted(resources, key=lambda r: r['order'])
