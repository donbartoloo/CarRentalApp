from django.db import models
from django.utils import timezone


class News(models.Model):
        photo = models.ImageField(default='news_default.jpg', upload_to='news_images/')
        title = models.TextField(default='title')
        text = models.TextField(default='text')
        date_created = models.DateTimeField(default=timezone.now)
        
        def __str__(self) -> str:
                return f'{self.title}'