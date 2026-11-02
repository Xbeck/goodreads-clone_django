from django.contrib import admin
from books.models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
	# pass
	search_fields = ('title', 'isbn')		# qidirish ni qo'shdik
	list_display = ('title', 'isbn', 'description')


class AuthorAdmin(admin.ModelAdmin):
	# pass
	search_fields = ('first_name', 'last_name')		# qidirish ni qo'shdik
	list_display = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
	# pass
	# search_fields = ('book.title', 'first_name', 'last_name')		# qidirish ni qo'shdik
	list_display = ('book', 'author')

class BookReviewAdmin(admin.ModelAdmin):
	# pass
	# search_fields = ('book', 'stars_given')		# qidirish ni qo'shdik
	list_display = ('book', 'stars_given', 'user')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)