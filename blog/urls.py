from django.urls import path

from .views import *

urlpatterns = [
    path('', RandomArticleView.as_view() , name='random'),
    path('show_all', showAll.as_view(), name='blog-showAll'),
    path('article/<int:pk>', ArticleView.as_view(), name='article' ),
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name='update_article'),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment'),
]