from urllib import response
from django.urls import reverse
from django.test import TestCase

from books.models import Book
from users.models import CustomUser


# Create your tests here.
class BooksTestCase(TestCase):
	# kitoblar yo'q bo'lgan holatni tekshiramiz, no book found  so'zi chiqishi kerak:
	def test_no_books(self):
		response = self.client.get(reverse('books:list'))

		# No books found.- teksimiz response ichida bor yo'qligiga javob berdi:
		self.assertContains(response, "No books found.")

	#  kitoblar ro'yxat bo'lganda hamma kitobning title lari chiqadimi yo yo'qmi shuni tekshiramiz:
	def test_books_list(self):
		# test boshida DB bo'sh bo'ladi, biz book yaratib olamiz:
		book1 = Book.objects.create(title="Book1", description="Description1", isbn="123456789")
		book2 = Book.objects.create(title="Book2", description="Description2", isbn="123456784")
		book3 = Book.objects.create(title="Book3", description="Description3", isbn="123456744")

		# so'rov yuboramiz:
		response = self.client.get(reverse('books:list') + "?page_size=2")

		# # DB dan barcha booklarni olamiz:
		# books = Book.objects.all()

		# har bir bookni title bor yo'qligini tekshiqramiz:
		for book in [book1, book2]:
			self.assertContains(response, book.title)
		self.assertNotContains(response, book3.title)		# 3 - kitob yo'qligini tekshiramiz

		# keyingi saxifadagi 3 chi kitobni borligini tekshiramiz:
		response = self.client.get(reverse('books:list') + '?page=2&page_size=2')
		self.assertContains(response, book3.title)

	# har bir kitobni saxifasidagi title va description borligini tekshiramiz:
	def test_detail_page(self):
		# bizga bitta kitob kerak bo'ladi:
		book = Book.objects.create(title="Book1", description="Description1", isbn="123456789")

		# request yuboramiz va unda book id ni nimaga tengligini ko'rsatamiz:
		response = self.client.get(reverse('books:detail', kwargs={"id": book.id}))

		# qaytgan javobda biz yaratgan book ni title va description i bormi yo'qmi  ligini tekshiramiz:
		self.assertContains(response, book.title)
		self.assertContains(response, book.description)

	def test_search_books(self):
		book1 = Book.objects.create(title="Sport", description="Description1", isbn="123456789")
		book2 = Book.objects.create(title="Guide", description="Description2", isbn="123456784")
		book3 = Book.objects.create(title="Shoe Dog", description="Description3", isbn="123456744")

		response = self.client.get(reverse("books:list") + "?q=sport")
		self.assertContains(response, book1.title)		# qidirgan kitob borligini tekshiradi
		self.assertNotContains(response, book2.title)		# kitob yo'qligini tekshiradi
		self.assertNotContains(response, book3.title)		# kitob yo'qligini tekshiradi

		response = self.client.get(reverse("books:list") + "?q=guide")
		self.assertContains(response, book2.title)		# qidirgan kitob borligini tekshiradi
		self.assertNotContains(response, book1.title)
		self.assertNotContains(response, book3.title)

		response = self.client.get(reverse("books:list") + "?q=shoe")
		self.assertContains(response, book3.title)		# qidirgan kitob borligini tekshiradi
		self.assertNotContains(response, book1.title)
		self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):
	def test_add_review(self):
		book = Book.objects.create(title="Sport", description="Description1", isbn="123456789")
		user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin", last_name="Abdukarimov", email="xab60xr@gmail.com")
		user.set_password("somepass")
		user.save()
		
		self.client.login(username="xolmumin", password="somepass")

		self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
			"stars_given": 3,
			"comment": "Nice book"
		})
		book_reviews = book.bookreview_set.all()		# bazadan barcha komentlarni olamiz

		self.assertEqual(book_reviews.count(), 1)		# bitta coment yozganmiz, shuning uchun bita komaent bo'lishi kerak
		self.assertEqual(book_reviews[0].stars_given, 3)		# berilgan star ni tekshiramiz
		self.assertEqual(book_reviews[0].comment, "Nice book")		# komentni tekshiramiz
		self.assertEqual(book_reviews[0].book, book)
		self.assertEqual(book_reviews[0].user, user)














