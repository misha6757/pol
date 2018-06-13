from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Author, Book, Comment
from .forms import CommentForm, AddAuthorForm, BookForm

def index(request):
	author = Author.objects.all()
	return render(request, 'books/index.html', {'author': author})

def detail(request, author_id):
	author = get_object_or_404(Author, id=author_id)
	books = Book.objects.filter(author_id=author_id)
	books.author = author
	return render(request, 'books/detail.html', {'books': books, 'author': author})

def description(request, author_id, book_id):
	form = CommentForm
	# author = get_object_or_404(Author, id=author_id)
	book = get_object_or_404(Book, author_id=author_id, id=book_id)
	comments = Comment.objects.filter(book_id=book_id)
	if request.user.is_authenticated:
		return render(request, 'books/description.html', 
			{'book': book, 'form': form, 'comments': comments})
	else:
		error_message = 'Только зарегистрированные могут оставлять комментарии.'
		return render(request, 'books/description.html', 
			{'book': book, 'form': form, 'comments': comments, 'error_message': error_message})

def all_books(request):
	books = Book.objects.all()

	return render(request, 'books/books.html', {'books': books})

def search(request):
	"""
	Поиск книг
	"""
	if 'q' in request.GET:
		q = request.GET['q']
		books = Book.objects.filter(title__icontains=q)
		return render(request, 'books/search.html', 
			{'books': books, 'query': q})
	else:
		return render(request, 'books/search.html', {'error': 'error_message', 'message': 'Unknown request'})

def add_comment(request, author_id, book_id):
	"""
	Добавление комментариев авторизованныи пользователями
	"""
	form = CommentForm(request.POST)
	# author = get_object_or_404(Author, id=author_id)
	book = get_object_or_404(Book, author_id=author_id, id=book_id)
	if request.method == 'POST' and request.user.is_authenticated:
		# Проверка 
		if form.is_valid():
			# Создание
			comment = form.save(commit=False)
			comment.book = book
			# Обновление
			comment.comment_text = request.POST['comment_text']
			username = request.user.get_username()
			comment.user_name = User.objects.get(username=username)
			# Сохранение
			comment.save()
	return HttpResponseRedirect(reverse('books:description', args=(book.author.id, book.id,)))
 

def add_author(request):
	"""
	Добавление авторов только авторизованными пользователями
	"""
	author = Author()
	form = AddAuthorForm
	if not request.user.is_authenticated:
		error_message = 'Только авторизованые пользователи могут добавлять новых авторов.'
		return render(request, 'books/author_form.html', 
			{'form': form, 'error_message': error_message})
	elif request.method == 'POST':
		form = AddAuthorForm(request.POST)
		if form.is_valid():
			author.writer = request.POST['writer']
			author.save()
		return HttpResponseRedirect(reverse('books:index'))
	return render(request, 'books/author_form.html', {'form': form})

def add_books(request):
	"""
	Добавление книги только авторизованными пользователями
	"""
	book = Book()
	form = BookForm
	# Спрятать, если пользователь не авторизован
	if not request.user.is_authenticated:	
		error_message = 'Только авторизованные пользователи могут добавлять книги.'
		return render(request, 'books/addbooks_form.html', 
			{'form': form, 'error_message': error_message})
	elif request.method == 'POST':
		form = BookForm(request.POST)
		writer = request.POST['author']
		author = Author.objects.get(id=int(writer))
		if form.is_valid():
			book.author = author
			book.title = request.POST['title']
			book.genre = request.POST['genre']
			book.year = request.POST['year']
			book.cover = request.POST['cover']
			book.save()
		return HttpResponseRedirect(reverse('books:all_books'))
	return render(request, 'books/addbooks_form.html', {'form': form})