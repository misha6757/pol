from django.forms import Textarea, ModelChoiceField, ModelForm
from .models import Comment, Author, Book
from django import forms


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text']
		widgets = {
            'comment_text': Textarea(attrs={'cols': 80, 'rows': 5, 'class' : 'form-control'}),
        }

class AddAuthorForm(ModelForm):
	class Meta:
		model = Author
		fields = ['writer']

class BookForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all())
    author = forms.Select(attrs={'class' : 'btn btn-primary dropdown-toggle', 'type' : 'button', 'data-toggle' : 'dropdown'})
    class Meta:
        model = Book
        fields = ['author', 'title', 'description', 'genre', 'year', 'cover']
        widgets = {
		    'author' : forms.Select(attrs={'class' : 'btn btn-primary dropdown-toggle', 'type' : 'button', 'data-toggle' : 'dropdown' }),
			'genre' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'}),
			'year' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'}),
			'cover' : forms.FileInput(attrs={'class' : 'col-md-12 form-control'}),
			'description' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'}),
            'title' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'})
        }