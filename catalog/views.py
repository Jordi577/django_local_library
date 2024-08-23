from django.shortcuts import render
# A view is a function, that processes an HTTP request, fetches data from the database,
# renders the data in an HTML page using HTML template, and then returns the generated
# HTML in an HTTP response to display the page to the user.

# Create your views here.

from .models import Book, Author, BookInstance, Genre
# For function based view simple add decorator @login_required
from django.contrib.auth.decorators import login_required
# For class based view
from django.contrib.auth.mixins import LoginRequiredMixin

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

    ### Session cookies: View count
    # Get a session value, setting a default if is not present
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    # Set a sesseion value e.g. increment in num_visits after vising index
    request.session['num_visits'] = num_visits

    # Deleting a session value
    # del request.session['num_visits']
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_books_with_genre': num_books_with_genre,
        'num_authors': num_authors,
        # Handing session dict to template
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    # Render accepts following parameters:
    #   1. the original HTTP request
    #   2. an html template with placeholders for the data
    #   3. a dict. containing the data to insert into the placeholders
    return render(request, 'index.html', context=context)

# class based view
from django.views import generic 
from django.contrib.auth.mixins import PermissionRequiredMixin

class SeeAllBorrowersView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_see_borrowers'
    model = BookInstance 
    template_name = 'catalog/borrowers_list.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class based view only available to current user """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class BookListView(LoginRequiredMixin, generic.ListView):
    # If user is not authenticated, user will be redirected to /login/
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

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

