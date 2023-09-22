
from django.http import HttpResponse
from .models import Article
from .forms import CommentForm
from django.views.generic import TemplateView, ListView,DetailView,View, CreateView, UpdateView, DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy , reverse
from django.db.models import Q 



class AboutPageView(TemplateView):
	""" widok związany z pokazywaniem strony about"""
	template_name = "about.html"

class HomePageView(ListView):
	""" widok związany z pokazywaniem listy artykułów"""
	model = Article
	template_name = "home.html"


# widok zwracany po wywołaniu GET
class ArticleDetailViewGet(DetailView):
	""" widok związany z pokazywaniem szczegółów artykułu"""
	model = Article
	template_name = "details.html"

	# dodajemy wyświetlanie formularza do komentowania
	def get_context_data(self, **kwargs): 
		""" funkcja zwraca formularz do komentowania"""
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context

#widok zwracany po wywołaniu POST
class ArticleDetailViewPost(SingleObjectMixin,FormView):
	""" widok związany z pokazywaniem szczegółów artykułu"""
	model = Article
	form_class = CommentForm
	template_name = "details.html"
	def post(self, request, *args, **kwargs):
		""" funkcja zapisuje komentarz do bazy danych"""
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)
	def form_valid(self, form):
		""" funkcja przypisuje obecnie zalogowanego usera do nowego obiektu Comment"""
		user = self.request.user 
		comment = form.save(commit=False)
		comment.article = self.object
		comment.author = user
		comment.save()
		return super().form_valid(form)
	def get_success_url(self):
		""" funkcja zwraca url do szczegółów artykułu"""
		article = self.get_object()
		return reverse("details", kwargs={"pk": article.pk})

# widok zwraca widoki dla GET lub POST
class ArticleDetailView(View):
	""" widok związany z pokazywaniem szczegółów artykułu """
	def get(self, request, *args, **kwargs):
		""" funkcja zwraca widok dla GET"""
		view = ArticleDetailViewGet.as_view()
		return view(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		""" funkcja zwraca widok dla POST"""
		view = ArticleDetailViewPost.as_view()
		return view(request, *args, **kwargs)


class ArticleCreateView(CreateView):
	""" widok związany z modelem Article"""
	model = Article
	template_name = "new.html"
	fields = ["title", "body","category","tag"]

	def form_valid(self, form):
		""" funkcja przypisuje obecnie zalogowanego usera do nowego obiektu Article"""
		f = form.save(commit=False)
		f.author = self.request.user
		f.save()
		return super().form_valid(form)

class ArticleUpdateView(UpdateView):
	""" widok związany z aktualizacją artykułu """
	model = Article
	template_name = "edit.html"
	fields = ["title", "body","category","tag"]


class ArticleDeleteView(DeleteView): 
	""" widok związany z usuwaniem artykułu """
	model = Article
	template_name = "delete.html"
	success_url = reverse_lazy("home")


class SignUpView(CreateView):
	""" widok związany z tworzeniem nowego użytkownika """
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"
