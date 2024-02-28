from django.test import TestCase, Client
from .models import News
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your tests here.

class NewsModelTest(TestCase):

    def test_create_multiple_news(self):
            for i in range(1000):
                news = News.objects.create(
                        title = f"test {i}",
                        text = f"test {i}",
                        date_created = timezone.now()
                )
            self.assertIsNotNone(news)
            self.assertIsInstance(news, News)
