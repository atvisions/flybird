from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # 文章列表和详情
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    
    # 分类相关
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # 评论相关
    path('<int:article_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # 文章操作
    path('<int:pk>/like/', views.ArticleLikeView.as_view(), name='article-like'),
    path('<int:pk>/publish/', views.ArticlePublishView.as_view(), name='article-publish'),
] 