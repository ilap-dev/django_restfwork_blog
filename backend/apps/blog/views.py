from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Post, Heading, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer
from core.permissions import HasValidAPIKey

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

#class PostListView(ListAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostListSerializer

class PostListView(APIView):
    #Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    permission_classes = [HasValidAPIKey]

    #Incluir que nuestra pagina web mantega una cache en redis, permitiendo que nuestra vista sea mas rapida
    #Sin embargo la actualizacion de las impresiones no se vera reflejada hasta que se elimine el cache
    #aqui se mantiene la cache por un minuto (60 * 1) y luego se elimina automaticamente
    @method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No Posts Found!")

            for post in posts:
                redis_client.incr(f"post:impressions:{post.id}")
                #increment_post_impressions.delay(post.id)

            serialized_posts = PostListSerializer(posts, many=True).data
        except Post.DoesNotExist:
            raise NotFound(detail="No Posts Found!")
        except Exception as e:
            raise APIException(detail=f"An Unexpected Error Ocurred: {str(e)}")

        return Response(serialized_posts)

#class PostDetailView(RetrieveAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer
#    lookup_field = 'slug'

class PostDetailView(RetrieveAPIView):
    # Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    permission_classes = [HasValidAPIKey]

    @method_decorator(cache_page(60 * 1))
    def get(self, request, slug):
        try:
            post = Post.postobjects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="The request Post does not exist")
        except Exception as e:
            raise APIException(detail=f"An Unexpected Error Ocurred: {str(e)}")
        serialized_post = PostSerializer(post).data

        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(
                detail="The Analytics Data for this Post does not exist")
        except Exception as e:
            raise APIException(
                detail=f"An Unexpected Error Ocurred While updating Post Analytics: {str(e)}")

        return Response(serialized_post)


class PostHeadingView(ListAPIView):
    # Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    permission_classes = [HasValidAPIKey]
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Heading.objects.filter(post__slug = post_slug)

class IncrementPostClickView(APIView):
    # Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    permission_classes = [HasValidAPIKey]

    def post(self,request):
        """Incrementa el contador de clicks de un post basado en su slug"""
        data = request.data
        try:
            post = Post.postobjects.get(slug=data['slug'])
        except Post.DoesNotExist:
            raise NotFound(detail="The request post does not exist")

        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(
                detail=f"An  Error Ocurred While updating Post Analytics: {str(e)}")
        return Response({
            "message":"Click Incremented Successfully",
            "clicks": post_analytics.clicks
        })