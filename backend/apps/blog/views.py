from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis
from django.conf import settings
from django.utils.decorators import method_decorator

#Hacer cache predeterminado (1 minuto) que se guarda en redis
from django.views.decorators.cache import cache_page

#Hacer cache personalizada que se guarda en redis
from django.core.cache import cache

from .models import Post, Heading, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer
from core.permissions import HasValidAPIKey
from .utils import get_client_ip
from .tasks import increment_post_view_task

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

#class PostListView(ListAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostListSerializer

class PostListView(StandardAPIView):
    #Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    #permission_classes = [HasValidAPIKey]

    def get(self, request, *args, **kwargs):
        try:
            #HACER CACHE PERSONALIZADA
            #Verificar si los datos que se requieren estan en una cache guardada
            cached_posts = cache.get("post_list")
            #si existe retornar la cache a la vista del usuario
            if cached_posts:
                for post in cached_posts:
                    # incrementar impressiones en redis
                    redis_client.incr(f"post:impressions:{post['id']}")
                return self.paginate(request, cached_posts)

            # si no existe, obtener los posts de la base de datos
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No Posts Found!")

            #Serializamos los datos de los posts
            serialized_posts = PostListSerializer(posts, many=True).data

            #Guardar datos de los posts/la vista del usuario en la cache llamada "post_list"
            cache.set("post_list", serialized_posts, timeout=(60 * 5) )

            for post in posts:
                #incrementar impressiones en redis
                redis_client.incr(f"post:impressions:{post['id']}")
                #increment_post_impressions.delay(post.id)

        except Exception as e:
            raise APIException(detail=f"An Unexpected Error Ocurred: {str(e)}")

        return self.paginate(request, serialized_posts)

#class PostDetailView(RetrieveAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer
#    lookup_field = 'slug'

class PostDetailView(StandardAPIView):
    # Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    #permission_classes = [HasValidAPIKey]

    def get(self, request):
        ip_address = get_client_ip(request)
        slug = request.query_params.get("slug")
        try:
            cached_post = cache.get(f"post_detail:{slug}")
            if cached_post:
                increment_post_view_task.delay(cached_post['slug'], ip_address)
                return self.response(cached_post)
            #sino esta en cache, obtener el post de la base de datos
            post = Post.postobjects.get(slug=slug)
            serialized_post = PostSerializer(post).data
            #Guardar el post en la cache
            cache.set(f"post_detail:{slug}", serialized_post, timeout=(60*5))

            # TODO Incrementar vistas en segundo plano
            increment_post_view_task.delay(post.slug, ip_address)

        except Post.DoesNotExist:
            raise NotFound(detail="The request Post does not exist")
        except Exception as e:
            raise APIException(detail=f"An Unexpected Error Ocurred HERE: {str(e)}")

        """try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(ip_address)
        except PostAnalytics.DoesNotExist:
            raise NotFound(
                detail="The Analytics Data for this Post does not exist")
        except Exception as e:
            raise APIException(
                detail=f"An Unexpected Error Ocurred While updating Post Analytics: {str(e)}")
        """

        return self.response(serialized_post)


class PostHeadingView(StandardAPIView):
    # Establecer un api key para permitir/denegar el uso de la solicitud HTTP
    #permission_classes = [HasValidAPIKey]
    def get(self, request):
        post_slug = request.query_params.get("slug")
        heading_objects = Heading.objects.filter(post__slug=post_slug)
        serialized_data = HeadingSerializer(heading_objects, many=True).data
        return self.response(serialized_data)

    # serializer_class = HeadingSerializer
    #HACER CACHE AUTOMATICA de 1 minuto
    # Incluir que nuestra pagina web mantega una cache en redis, permitiendo que nuestra vista sea mas rapida
    # Sin embargo las actualizaciones no se veran reflejadas hasta que se elimine el cache
    # aqui se mantiene la cache por un minuto (60 * 1) y luego se elimina automaticamente
    #@method_decorator(cache_page(60 * 1))
    #def get_queryset(self):
        #post_slug = self.kwargs.get('slug')
        #return Heading.objects.filter(post__slug = post_slug)

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