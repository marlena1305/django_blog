from django.db import models
from django.urls import reverse
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
    "auth.User",
    on_delete=models.CASCADE,
    )

    date = models.DateTimeField(auto_now_add=True)

    body = models.TextField()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("details", kwargs={"pk": self.pk})


class Comment(models.Model): 
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey("auth.User",
    on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.comment
    def get_absolute_url(self):
        return reverse("article_list")