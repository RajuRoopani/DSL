from django.http import HttpResponse
from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer


def dummy_view(request):
    return HttpResponse('roadmap placeholder')


from django.shortcuts import render


def generate_view(request):
    return render(request, 'roadmap/generate.html')


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


from .models import Topic, Resource
from .serializers import TopicSerializer, ResourceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


@api_view(['GET'])
def generate_roadmap_api(request, skill_id):
    """Return topics and resources for a given skill id."""
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Skill.DoesNotExist:
        return Response({'detail': 'Skill not found'}, status=404)

    topics = Topic.objects.filter(skill=skill)
    data = []
    for t in topics:
        resources = Resource.objects.filter(topic=t)
        data.append({
            'topic': TopicSerializer(t).data,
            'resources': ResourceSerializer(resources, many=True).data,
        })
    return Response({'skill': SkillSerializer(skill).data, 'topics': data})
