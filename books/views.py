from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
# from matplotlib.style import use
from books.forms import BookReviewForm


from books.models import Book, BookReview


# Create your views here.

# class BooksView(ListView):
# 	template_name = "books/list.html"
# 	queryset = Book.objects.all()
# 	context_object_name = "books"
# 	paginate_by: int = 2

class BooksView(View):
	def get(self, request):
		books = Book.objects.all().order_by('id')
		search_query = request.GET.get('q', '')
		if search_query:
			books = books.filter(title__icontains=search_query)

		page_size = request.GET.get('page_size', 4)		# element soni kiritilmasa har bir saxifaga 2 tadan element joylaydi.
		paginator = Paginator(books, page_size)

		page_num = request.GET.get('page', 1)
		page_obj = paginator.get_page(page_num)

		return render(
			request,
			"books/list.html",
			{"page_obj": page_obj, "search_query": search_query}
		)
		# return render(request, "books/list.html", {"books": books})


# class BookDetailView(DetailView):
# 	model = Book
# 	template_name = 'books/detail.html'
# 	pk_url_kwarg = "id"

class BookDetailView(View):
	def get(self, request, id):
		book = Book.objects.get(id=id)
		review_form = BookReviewForm()

		return render(request, "books/detail.html", {"book": book, "review_form": review_form})


class AddReviewView(LoginRequiredMixin, View):
	def post(self, request, id):
		book = Book.objects.get(id=id)		# kitobni bazadan olib olamiz
		review_form = BookReviewForm(data=request.POST)  	# formani olamiz

		if review_form.is_valid():
			BookReview.objects.create(
				book=book,
				user=request.user,
				stars_given=review_form.cleaned_data['stars_given'],
				comment=review_form.cleaned_data['comment']

			)
			return redirect(reverse("books:detail", kwargs={"id": book.id}))

		return render(request, "books/detail.html", {"book": book, "review_form": review_form})
