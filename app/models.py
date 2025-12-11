from django.db import models
from django.contrib.auth.models import User


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class PostModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    viewer = models.IntegerField(default=1)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, upload_to="posts/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return (
            f"{self.message} is written by {self.author.username} in {self.post.title}"
        )
