from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid


class Genre(models.Model):
    """LocalLibrary books have a genre which is represented by this model."""
    name = models.CharField(
               max_length=200,
               help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)'
    )
    def __str__(self):
        return self.name


class Language(models.Model):
    """LocalLibrary books have a language which is represented by this model."""
    name = models.CharField(
               max_length=200,
               help_text='Enter the book\'s natural language (e.g. English (South Africa), Tswana, Zulu etc.)'
    )
    def __str__(self):
        return self.name


class Book(models.Model):
    """Books within the LocalLibrary are represented by this model."""
    title = models.CharField(
                max_length=200,
                help_text='Enter the book\'s title'
    )
    author = models.ForeignKey(
                 'Author',
                 on_delete=models.SET_NULL,
                 null=True
    )
    summary = models.TextField(
                  max_length=1000,
                  help_text='Enter a brief description of the book'
    )
    isbn = models.CharField(
               'ISBN',
               max_length=13,
               unique=True,
               help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(
                Genre,
                help_text='Select a genre for this book'
    )
    language = models.ForeignKey(
                   'Language',
                   on_delete=models.SET_NULL,
                   null=True
    )
    
    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class BookInstance(models.Model):

    id = models.UUIDField(
             primary_key=True,
             default=uuid.uuid4,
             help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(
               Book,
               on_delete=models.RESTRICT
    )
    imprint = models.CharField(
                  max_length=7,
                  help_text='This identifies a particular publisher or registrant. May be up to 7 digits.'
    )
    due_back = models.DateField(
                   null=True,
                   blank=True
    )
    borrower = models.ForeignKey(
                   User,
                   on_delete=models.SET_NULL,
                   null=True,
                   blank=True
    )
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
                 max_length=1,
                 choices=LOAN_STATUS,
                 blank=True,
                 default='m',
                 help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):

    first_name = models.CharField(
                     max_length=100,
                     null=True,
                     blank=True
    )
    surname = models.CharField(
                  max_length=100,
                  null=True,
                  blank=True
    )
    date_of_birth = models.DateField(
                        'Birth Date',
                        null=True,
                        blank=True
    )
    date_of_death = models.DateField(
                        'death date',
                        null=True,
                        blank=True
    )

    class Meta:
        ordering = ['surname', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # return f'{self.surname}, {self.first_name}'
        return '{0}, {1}'.format(self.surname, self.first_name)
