from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    # symmetrical means that we can follow somebody, and they don't have to follow us back, they can but don't have to,
    # blank means that we don't have to follow anybody
    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.user.username


# Create Profile when New User Signs Up
# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


# does the same thing as a receiver
post_save.connect(create_profile, sender=User)


class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    genre = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    isbn = models.IntegerField()
    # isbn = models.CharField(max_length=13)
    count = models.IntegerField(null=True, default=0)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
