# Generated by Django 4.2.17 on 2025-01-11 12:07

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("slug", models.SlugField(unique=True, verbose_name="URL标识")),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        upload_to="articles/covers/%Y/%m/",
                        verbose_name="封面图",
                    ),
                ),
                ("summary", models.TextField(blank=True, verbose_name="摘要")),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="内容"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "草稿"), ("published", "已发布")],
                        default="draft",
                        max_length=10,
                        verbose_name="状态",
                    ),
                ),
                (
                    "views",
                    models.PositiveIntegerField(default=0, verbose_name="浏览量"),
                ),
                (
                    "likes",
                    models.PositiveIntegerField(default=0, verbose_name="点赞数"),
                ),
                (
                    "is_featured",
                    models.BooleanField(default=False, verbose_name="是否推荐"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "published_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="发布时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="分类名称")),
                ("slug", models.SlugField(unique=True, verbose_name="分类标识")),
                ("description", models.TextField(blank=True, verbose_name="分类描述")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
            ],
            options={
                "verbose_name": "分类",
                "verbose_name_plural": "分类",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="是否公开"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="articles.article",
                        verbose_name="文章",
                    ),
                ),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "ordering": ["-created_at"],
            },
        ),
    ]
