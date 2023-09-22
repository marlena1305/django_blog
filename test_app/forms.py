from django import forms
from .models import Comment, Article, Category, Tag
class CommentForm(forms.ModelForm):
    """ formularz do komentowania artykułu"""
    class Meta:
       """ klasa opisująca model formularza"""
       model = Comment
       fields = ("comment",)


