from django.test import TestCase
from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from test_app.models import Article, Category, Tag,ArticleStyle
from django.contrib.auth.models import User
from django.test import Client



@pytest.fixture
def create_article(create_user, create_category, create_tag,create_style):
    """ fixture tworzący artykuł"""
    user = create_user(username="testuser", password="testpassword")
    category = create_category(category_name="Test Category")
    style = create_style(background_color="orange")

    tags = [create_tag(tag_name="Tag 1", color="Red"), create_tag(tag_name="Tag 2", color="Blue")]

    def _create_article(title="Test Article", author=user, category=category, tags=tags,style=style, body="This is a test article body."):
        """ funcja tworząca artykuł"""
        a = Article.objects.create(
            title=title,
            author=author,
            category=category,
            style = style,
            body=body
        )
        a.tag.set(tags)

        return a
    return _create_article

@pytest.fixture
def create_style():
    """ fixture tworzący styl artykułu"""
    def _create_style(background_color="orange"):
        """ funcja tworząca styl artykułu"""
        return ArticleStyle.objects.create(background_color=background_color)

    return _create_style


@pytest.fixture
def create_category():
    """ fixture tworzący kategorię"""
    def _create_category(category_name="Test Category"):
        """ funcja tworząca kategorię"""
        return Category.objects.create(category=category_name)

    return _create_category

@pytest.fixture
def create_tag():
    """ fixture tworzący tag"""
    def _create_tag(tag_name="Tag 1", color="Red"):
        """ funcja tworząca tag"""
        return Tag.objects.create(tag=tag_name, color=color)

    return _create_tag

@pytest.fixture
def create_user():
    """ fixture tworzący użytkownika"""
    def _create_user(username="testuse",email = "'kowalski@poczta.onet.pl'", password="Qwed234rf0sf"):
        """ funcja tworząca użytkownika"""
        return User.objects.create_user(username,email,password)

    return _create_user

@pytest.mark.django_db
def test_article_creation(create_article):
    """ test sprawdzający czy artykuł został utworzony poprawnie"""
    article = create_article()

  
    assert Article.objects.count() == 1
    assert article.title == "Test Article"
    assert str(article.author) == "testuser"
    assert str(article.category) == "Test Category"
    assert sorted([str(tag) for tag in article.tag.all()]) == ["Tag 1", "Tag 2"]
    assert article.body == "This is a test article body."
    

@pytest.mark.django_db
def test_article_absolute_url(create_article):
    """ test sprawdzający czy funkcja get_absolute_url zwraca poprawny url"""
    article = create_article()

    expected_url = reverse("details", kwargs={"pk": article.pk})
    assert article.get_absolute_url() == expected_url

@pytest.mark.django_db
def test_article_str_representation(create_article):
    """ test sprawdzający czy funkcja __str__ zwraca poprawny string"""
    article = create_article()
    assert str(article) == "Test Article"


class AboutViewTestCase(TestCase):
    """ testy dla widoku about """
    def test_about_view_returns_blog(self):
        """ test sprawdzający czy widok about zwraca ciąg 'Blog' """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")

    def test_about_view_uses_correct_template(self):
        """ test sprawdzający czy widok about wykorzystuje odpowiedni template"""
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'about.html')

class HomeViewTestCase(TestCase):
    """ testy dla widoku home """
    def test_home_view_returns_hello_world(self):
        """ test sprawdzający czy widok about zwraca ciąg 'Blog' """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")

    def test_home_view_uses_correct_template(self):
        """ test sprawdzający czy widok home wykorzystuje odpowiedni template"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class ArticleCreateViewTestCase(TestCase):
    """ testy dla widoku new """

    def test_new_view(self):
        """ test sprawdzający czy widok new zwraca ciąg 'Blog' """
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")

    def test_new_view_uses_correct_template(self):
        """ test sprawdzający czy widok new wykorzystuje odpowiedni template"""
        response = self.client.get(reverse('new'))
        self.assertTemplateUsed(response, 'new.html')

def create_test_article():
    """ funkcja tworząca artykuł"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    category = Category.objects.create(category="Test Category")
    tag1 = Tag.objects.create(tag="Tag 1", color="Red")
    tag2 = Tag.objects.create(tag="Tag 2", color="Blue")
    style = ArticleStyle.objects.create(background_color="orange")
    
    a=Article.objects.create(
        title="Test Article",
        author=user,
        category=category,
        style=style,
        body="This is a test article body.",
    )
    a.tag.set([tag1, tag2])
    return a

class ArticleUpdateViewTestCase(TestCase):
    """ testy dla widoku update """
    def test_article_update_view(self):
        """ test sprawdzający czy widok update"""
        article = create_test_article()
        response = self.client.get(reverse('edit', kwargs={'pk': article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog')  
        self.assertTemplateUsed(response, 'edit.html')

    def test_update_view_uses_correct_template(self):
        """ test sprawdzający czy widok update wykorzystuje odpowiedni template"""
        article = create_test_article()
        response = self.client.get(reverse('edit', kwargs={'pk': article.pk}))
        self.assertTemplateUsed(response, 'edit.html')



class SignupViewTestCase(TestCase):
    """ testy dla widoku signup """

    def test_signup_view(self):
        """ test sprawdzający czy widok signup zwraca ciąg 'Blog' """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")

    def test_signup_view_uses_correct_template(self):
        """ test sprawdzający czy widok signup wykorzystuje odpowiedni template"""
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')


class ArticleDetailViewTestCase(TestCase):
    """ testy dla widoku details """


    def test_article_details_view(self):
        """ test sprawdzający czy widok details zwraca ciąg 'Blog' """
        article = create_test_article()       
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(str(article.author), "testuser")
        self.assertEqual(str(article.category), "Test Category")
        self.assertEqual(sorted([str(tag) for tag in article.tag.all()]), ["Tag 1", "Tag 2"])
        self.assertEqual(article.body, "This is a test article body.")

        response = self.client.get(reverse('details', kwargs={'pk': article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog')  
       
    def test_details_view_uses_correct_template(self):
        """ test sprawdzający czy widok details wykorzystuje odpowiedni template"""
        article = create_test_article()
        response = self.client.get(reverse('details', kwargs={'pk': article.pk}))
        self.assertTemplateUsed(response, 'details.html')


class ArticleDeleteViewTestCase(TestCase):
    """ testy dla widoku delete """

    def test_article_delete_view(self):
        """ test sprawdzający czy widok delete"""
        article = create_test_article()
        response = self.client.get(reverse('delete', kwargs={'pk': article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog')  
        self.assertTemplateUsed(response, 'delete.html')

    def test_delete_view_uses_correct_template(self):
        """ test sprawdzający czy widok delete wykorzystuje odpowiedni template"""
        article = create_test_article()
        response = self.client.get(reverse('delete', kwargs={'pk': article.pk}))
        self.assertTemplateUsed(response, 'delete.html')