from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Heading, PostView
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer
from .utils import get_client_ip

#class PostListView(ListAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostListSerializer

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.postobjects.all()
        serialized_posts = PostListSerializer(posts, many=True).data
        return Response(serialized_posts)

#class PostDetailView(RetrieveAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer
#    lookup_field = 'slug'

class PostDetailView(RetrieveAPIView):
    def get(self, request, slug):
        post = Post.postobjects.get(slug=slug)
        serialized_post  = PostSerializer(post).data
        client_ip = get_client_ip(request)

        if PostView.objects.filter(post=post, ip_address = client_ip).exists():
            return Response(serialized_post)

        PostView.objects.create(post=post, ip_address = client_ip)
        return Response(serialized_post)



class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Heading.objects.filter(post__slug = post_slug)