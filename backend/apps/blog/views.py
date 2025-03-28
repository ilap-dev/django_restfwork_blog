
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Post
from .serializers import PostListSerializer, PostSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'