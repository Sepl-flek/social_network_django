from django.db.models import Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from post.models import Post, UserPostRelation
from post.permissions import IsOwnerOrStaffOrReadOnly
from post.serializers import PostSerializer, UserPostRelationSerializer


# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().annotate(rating=Avg('user_post_relations__rating'))
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['data']
    filterset_fields = ['owner']
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

class UserPostRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserPostRelation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserPostRelationSerializer
    lookup_field = 'post'

    def get_object(self):
        obj, created = UserPostRelation.objects.get_or_create(user=self.request.user,
                                                              post_id=self.kwargs['post'])
        return obj
def auth(request):
    return render(request, 'auth.html')