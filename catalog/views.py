from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    STATUS_AVAILABLE = 'a'
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=STATUS_AVAILABLE).count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_warrior_books = Book.objects.filter(summary__icontains='warrior').count()
    num_in_books = Book.objects.filter(title__icontains='in').count()

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
                },
    )
