from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

STATUS_AVAILABLE = 'a'
STATUS_ON_LOAN = 'o'
def index(request):
    """
    View function for home page of site.
    """
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=STATUS_AVAILABLE).count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_warrior_books = Book.objects.filter(summary__icontains='warrior').count()
    num_in_books = Book.objects.filter(title__icontains='in').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context={'num_books' : num_books, 
                'num_instances' : num_instances,
                'num_instances_available': num_instances_available,
                'num_genres' : num_genres,
                'num_authors' : num_authors,
                'num_warrior_books' : num_warrior_books,
                'num_in_books' : num_in_books,
                'num_visits' : num_visits
                },
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact=STATUS_ON_LOAN).order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_view_all_checkouts'
    """ Generic class-based view listing books on loan with borrower"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 5
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact=STATUS_ON_LOAN).order_by('due_back')