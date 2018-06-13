from django.db import models
from django.contrib.auth.models import User


# GENRE_CHOICES = (
# 	('Фантастика'),
# 	('Ужастика'),
# 	('Исторический'))

class Author(models.Model):
    writer = models.CharField(u'Автор', max_length=200)
    verbose_name = (u'Автор')

    def __str__(self):
        return self.writer

class Book(models.Model):
	author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=u'Автор')
	title = models.CharField('Наименование', max_length=250)
	genre = models.CharField('Жанр', max_length=50)
	description = models.TextField('Описание')
	year = models.IntegerField('Год издания')
	cover = models.ImageField('Обложка', upload_to='static/static_dirs/images/', blank=True)

	
	def __str__(self):
		return self.title + ' (' + str(self.year) + ')'

class Comment(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	comment_text = models.CharField('Текст комментария', max_length=500)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.comment_text