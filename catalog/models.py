from django.db import models
from django.urls import reverse
from django.conf import settings
from datetime import date

# class MyModelName(models.Model):
#     """A typical class defining a model, derived from the Model class."""

#     # Fields
#     # help_text provides a text label for HTML forms
#     my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')

#     # Model-level metadata
#     class Meta:
#         # Reverses the chronological order of the model
#         ordering = ['-my_field_name']
#         # ordering = ['title', '-pubdate']

#     # Methods
#     # https://stackoverflow.com/questions/43179875/when-to-use-django-get-absolute-url-method
#     def get_absolute_url(self):
#         """Returns the URL to access a particular instance of MyModelName."""
#         return reverse('model-detail-view', args=[str(self.id)])

#     # Method to return a human-readable string for each object
#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site etc.)."""
#         return self.my_field_name

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [UniqueConstraint(Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message = "Genre already exists (case insensitive match)"),]

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200, unique=True,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [UniqueConstraint(Lower('name'), name='language_name_case_insensitive_unique', violation_error_message = "Language already exists (case insensitive match)"),]

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.
    # One-To-Many Relationship
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn''">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title
        
    # Genre has a ManyToMany-Relationship with Book. Django
    # prevents this, because of the cost of doing so. Instead
    # we have to define our own get_genre_name function.
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    # This will be displayed in the admin interface
    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
import uuid # Required for unique book instances

class BookInstance(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'), 
        ('o', 'On loan'), 
        ('a', 'Available'), 
        ('r', 'Reserved'),
        )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability',)

    class Meta:
        ordering = ['due_back']
        # Each permission can be defined in a tuple containing a permission name and a display value
        permissions = (
            ("can_mark_returned", "Set book as returned"),
            ("can_see_borrowers", "See all borrowers"),
                       )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

