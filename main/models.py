from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify, truncatechars
from django_resized import ResizedImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    # symmetrical means that we can follow somebody, and they don't have to follow us back, they can but don't have to,
    # blank means that we don't have to follow anybody
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=1000)
    homepage_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)
    linkedin_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self) -> str:
        return self.user.username

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #     img = Image.open(self.profile_image.path)
    #     if img.width > 480 or img.height > 480:
    #         output_size = (480, 480)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_image.path)


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

    def __str__(self) -> str:
        return self.title


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_input = models.TextField(verbose_name="User Input", null=True)  # This is the user query.
    ai_response = models.TextField(verbose_name="User Input", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # This will store the time of each message input and response.

    class Meta:
        verbose_name = 'Chat'


# create tweets model
class Tweet(models.Model):
    user = models.ForeignKey(User, related_name="tweets", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)

    # keep track or count of likes
    def number_of_likes(self):
        return self.likes.count()

    # return amount of likes in admin
    def get_likes(self):
        return len([like for like in self.likes.all()])

    # displays renamed get_likes method in admin
    get_likes.short_description = 'Likes'

    # return short version (100 characters) of body in admin
    @property
    def short_body(self):
        return truncatechars(self.body, 100)


    def __str__(self) -> str:
        return f'{self.user}'

    # def __str__(self):
    #     return (
    #         f'{self.user} '
    #         f'({self.created_at:%Y-%m-%d %H:%M}): '
    #         f'{self.body}...'
    #     )

    class Meta:
        ordering = ["-created_at"]



