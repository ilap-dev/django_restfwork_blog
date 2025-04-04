from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostHeadingView,
                    IncrementPostClickView)

urlpatterns = [
    path('posts/',PostListView.as_view(), name='post-list'),
    path('posts/<slug>/',PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug>/headings/',PostHeadingView.as_view(), name='post-headings'),
    path('posts/increment_click/',IncrementPostClickView.as_view(), name='increment-post-click'),
]