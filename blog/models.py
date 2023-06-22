from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    count = models.IntegerField(null=True)

    tags = TaggableManager()

    @property
    def short_title(self):
        return truncatechars(self.title, 80)


    def get_absolute_url(self):
        return reverse('post_single', args=[self.slug])

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
