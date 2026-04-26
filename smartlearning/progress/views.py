from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import Progress
from .serializers import ProgressSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise only the owner may edit
        return obj.user == request.user


def dummy_view(request):
    return HttpResponse('progress placeholder')


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Override to return the user's aggregated total XP after creating a progress entry
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        total = Progress.objects.filter(user=request.user).aggregate(total_xp=Sum('xp'))['total_xp'] or 0
        resp_data = {
            'id': serializer.data.get('id'),
            'xp': serializer.data.get('xp'),
            'total_xp': total,
        }
        return Response(resp_data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def leaderboard(request):
    # Aggregate top users by XP
    agg = (
        Progress.objects.values('user', 'user__username')
        .annotate(total_xp=Sum('xp'))
        .order_by('-total_xp')[:10]
    )
    # normalize keys for the frontend
    result = [
        {
            'user': a['user'],
            'username': a.get('user__username') or f'User {a["user"]}',
            'total_xp': a['total_xp'],
        }
        for a in agg
    ]
    return Response(result)
