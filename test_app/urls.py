from django.urls import path,include
from test_app import views
from .views import AboutPageView,ListPageView,ArticleDetailView,ArticleCreateView,ArticleUpdateView,ArticleDeleteView,SignUpView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("", ListPageView.as_view(), name="home"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="details"), 
    path("article/new/", ArticleCreateView.as_view(), name="new"),
    path("article/<int:pk>/edit/", ArticleUpdateView.as_view(), name="edit"),
    path("article/<int:pk>/delete/", ArticleDeleteView.as_view(),name="delete"),
    path("accounts/", include("django.contrib.auth.urls")), # new
    path("signup/", SignUpView.as_view(), name="signup"),
]