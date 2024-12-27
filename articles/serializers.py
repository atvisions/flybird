from rest_framework import serializers
from .models import Article, Category, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 
            'content', 
            'author', 
            'author_name',
            'article', 
            'is_public',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['author', 'article', 'created_at', 'updated_at']

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'cover',
            'summary',
            'content',
            'status',
            'views',
            'likes',
            'is_featured',
            'author',
            'author_name',
            'category',
            'category_name',
            'comments',
            'comment_count',
            'created_at',
            'updated_at',
            'published_at'
        ]
        read_only_fields = [
            'author', 
            'views', 
            'likes', 
            'created_at', 
            'updated_at', 
            'published_at'
        ] 