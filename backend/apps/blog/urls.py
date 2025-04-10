from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostHeadingView,
                    IncrementPostClickView,
                    GenerateFakePostsView,
                    GenerateFakeAnalyticsView
                    )

urlpatterns = [
    path('generate_posts/',GenerateFakePostsView.as_view()),
    path('generate_analytics/',GenerateFakeAnalyticsView.as_view()),
    path('posts/',PostListView.as_view(), name='post-list'),
    path('posts/',PostListView.as_view(), name='post-list'),
    path('post/',PostDetailView.as_view(), name='post-detail'),
    path('post/headings/',PostHeadingView.as_view(), name='post-headings'),
    path('post/increment_click/',IncrementPostClickView.as_view(), name='increment-post-click'),
]