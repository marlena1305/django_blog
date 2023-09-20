
from django.http import HttpResponse
from .models import Article
from .forms import CommentForm
from django.views.generic import TemplateView, ListView,DetailView,View, CreateView, UpdateView, DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy , reverse
from django.db.models import Q 

def home(request):
    return HttpResponse("Blog")

class AboutPageView(TemplateView):
	template_name = "about.html"

class ListPageView(ListView):
	model = Article
	template_name = "list.html"


# widok zwracany po wywołaniu GET
class ArticleDetailViewGet(DetailView):
	model = Article
	template_name = "details.html"

	# dodajemy wyświetlanie formularza do komentowania
	def get_context_data(self, **kwargs): 
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context

#widok zwracany po wywołaniu POST
class ArticleDetailViewPost(SingleObjectMixin,FormView):
	model = Article
	form_class = CommentForm
	template_name = "details.html"
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)
	def form_valid(self, form):
		user = self.request.user 
		comment = form.save(commit=False)
		comment.article = self.object
		comment.author = user
		comment.save()
		return super().form_valid(form)
	def get_success_url(self):
		article = self.get_object()
		return reverse("details", kwargs={"pk": article.pk})

# widok zwraca widoki dla GET lub POST
class ArticleDetailView(View):
	def get(self, request, *args, **kwargs):
		view = ArticleDetailViewGet.as_view()
		return view(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		view = ArticleDetailViewPost.as_view()
		return view(request, *args, **kwargs)


class ArticleCreateView(CreateView):
	model = Article
	template_name = "new.html"
	fields = ["title", "body"]

	def form_valid(self, form):
		f = form.save(commit=False)
		f.author = self.request.user
		f.save()
		return super().form_valid(form)

class ArticleUpdateView(UpdateView):
	model = Article
	template_name = "edit.html"
	fields = ["title", "body"]


class ArticleDeleteView(DeleteView): 
	model = Article
	template_name = "delete.html"
	success_url = reverse_lazy("home")


class SignUpView(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"
