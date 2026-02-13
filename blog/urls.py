from django.urls import path

from .views import showAll, ArticleView, RandomArticleView

urlpatterns = [
    path('', RandomArticleView.as_view() , name='random'),
    path('show_all', showAll.as_view(), name='blog-showAll'),
    path('article/<int:pk>', ArticleView.as_view(), name='article' )
    
]