from django.core.paginator import Paginator
# from django.http import HttpResponse
from django.shortcuts import render

from books.models import BookReview


def landing_page(request):
	# print(request.COOKIES['sessionid'])		# user uchun cookidagi sesiya id sini chiqaradi
	# print(request.user.is_authenticated)		# request jo'natayotgan user login qilganmi degan savolga javob beradi
	return render(request, "landing_page.html")
	# return HttpResponse(f"Django ishga tushdi: {request.META['HTTP_USER_AGENT']}")


def home_page(request):
	book_reviews = BookReview.objects.all().order_by('-created_at') 	# teskari tartibda chiqaramiz, eng oxirgisi birnchida turadi.
	page_size = request.GET.get('page_size', 10)
	paginator = Paginator(book_reviews, page_size)

	page_num = request.GET.get('page', 1)
	page_object = paginator.get_page(page_num)
	
	# return render(request, "home.html", {"book_reviews": book_reviews})
	return render(request, "home.html", {"page_obj": page_object})
