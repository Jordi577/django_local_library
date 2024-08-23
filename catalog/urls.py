from django.urls import path
from . import views

urlpatterns = [
    # The path() function is responsible for three things:
    #   1. A URL pattern, which is en emptry string in this case
    #   2. A view function that will be called if the URL pattern is detected
    #   3. Specifying a name parameter, which is a unique parameter to use in reverse mapping
    # <a href="{% url 'index' %}">Home</a>. (Dynamically calling 'index')
    path('', views.index, name='index'),
]

urlpatterns += [
    # The URL pattern in this case is 'catalog/books/'
    # A view function will if the URL matches views.BookListView.as_view
    # With name 'books' for URL mapping {% url 'books' %}
    #   The handler .as_view() does all the work by creating an instance of the class, and
    #   making sure the right handler methods are called for incoming http requests.
    path('books/', views.BookListView.as_view(), name='books'),]

urlpatterns += [
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors'),
]

urlpatterns += [
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(),
        name='my-borrowed')
]

urlpatterns += [
    path('borrowers/', views.SeeAllBorrowersView.as_view(),
        name='borrowers-list')
]