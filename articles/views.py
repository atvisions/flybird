from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Article, Category, Comment
from .serializers import (
    ArticleSerializer, 
    CategorySerializer,
    CommentSerializer
)

class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_id'])

    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(author=self.request.user, article=article)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.likes += 1
        article.save()
        return Response({'likes': article.likes}, status=status.HTTP_200_OK)

class ArticlePublishView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.status = 'published'
        article.published_at = timezone.now()
        article.save()
        return Response({'status': 'published'}, status=status.HTTP_200_OK) 