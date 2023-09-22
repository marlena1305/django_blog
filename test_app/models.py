from django.db import models
from django.urls import reverse

class Tag(models.Model): 
    """ model opisujący tag przypisany do artykułu"""
    tag = models.CharField(max_length=140)
    color = models.CharField(max_length=10)

    def __str__(self):
        """ funkcja zwraca string"""
        return self.tag
    def get_absolute_url(self):
        """ funckja zwraca url"""
        return reverse("article_list")
    

class Category(models.Model):
    """ model opisujący kategorię artykułu""" 
    category = models.CharField(max_length=140)
    def __str__(self):
        """ funkcja zwraca string"""
        return self.category
    def get_absolute_url(self):
        """ funckja zwraca url"""
        return reverse("article_list")
    
class Article(models.Model):
    """ model opisujący artykuł """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
    "auth.User",
    on_delete=models.CASCADE,
    )

    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    tag = models.ManyToManyField(Tag)

    body = models.TextField()
    def __str__(self):
        """ funkcja zwraca string """
        return self.title
    def get_absolute_url(self):
        """ funckja zwraca url """
        return reverse("details", kwargs={"pk": self.pk})


class Comment(models.Model): 
    """ model opisujący komentarz """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey("auth.User",
    on_delete=models.CASCADE,
    )
    def __str__(self):
        """ funkcja zwraca string """
        return self.comment
    def get_absolute_url(self):
        """ funckja zwraca url """
        return reverse("article_list")
    
