import factory
import faker
from django.contrib.auth.models import User

from .models import Book


FAKE = faker.Faker()


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=8)  # sentence is type of data what we want to actually insert
    slug = factory.Faker('slug')
    genre = factory.Faker('sentence', nb_words=3)  # nb is number of words we want to insert
    author = User.objects.get_or_create(username='admin')[0]
    isbn = factory.LazyAttribute(lambda x: faker.generator.random.randrange(1E+12, 1E+13))


# Factory Boy and Faker is going to provide us tools to automatically generate data
# and for us to be able to specify how much data we want to insert into our database
