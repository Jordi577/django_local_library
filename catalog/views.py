from django.shortcuts import render
# A view is a function, that processes an HTTP request, fetches data from the database,
# renders the data in an HTML page using HTML template, and then returns the generated
# HTML in an HTTP response to display the page to the user.

# Create your views here.

from .models import Book, Author, BookInstance, Genre

# function based view
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Model class "Book" has parameter "Genre", which has parameter "name". iexact is caseinsensitive. 
    # More information for db queries: https://docs.djangoproject.com/en/5.1/topics/db/queries/
    num_books_with_genre = Book.objects.filter(genre__name__iexact='fantasy').count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_books_with_genre': num_books_with_genre,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    # Render accepts following parameters:
    #   1. the original HTTP request
    #   2. an html template with placeholders for the data
    #   3. a dict. containing the data to insert into the placeholders
    return render(request, 'index.html', context=context)

# class based view
from django.views import generic 

class BookListView(generic.ListView):
    # The generic view will query the database to get all records for the specified model
    # then render a template located at /catalog/templates/catalog/book_list.html 
    # Within the template we can acess the list of books with the template 
    # i.e. generically <the model name>_list
    model = Book 

    # we can also specify a different template location with 
    # template_name = 'books/my_arbitrary_template_name_list.html'
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books 
    # and if book_list is not intuitive enough we can write 
    context_object_name = 'book_list'

    # We can also override methods
    # def get_queryset(self):
    #     # Get 5 books containing the title war
    #     return Book.objects.filter(title__icontains='war')[:5] 
    
    # we might also override get_context_data() in order to pass additional context
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context
    
    # When doing this it is important to follow the pattern used above:
    #   First get the existing context from our superclass.
    #   Then add your new context information.
    #   Then return the new (updated) context.

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

