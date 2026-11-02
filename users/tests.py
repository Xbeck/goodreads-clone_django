from urllib import response
from django.contrib.auth import get_user
# from django.contrib.auth.models import User		# jango user modeli endi kerak mas, chunki uni o'zgartirib bo'lmaydi, uning o'rniga o'zimiz yaratgan customuser ni ishlatamiz
from users.models import CustomUser

from django.test import TestCase
from django.urls import reverse
# from matplotlib.pyplot import cla, clabel


# Create your tests here.
class RegistrationTestCase(TestCase): # test uchun user yaratamiz
	def test_user_account_is_created(self):
		self.client.post(
			reverse("users:register"),
			data={
				"username": "xolmumin",
				"first_name": "Xolmumin",
				"last_name": "Abdukarimov",
				"email": "xab60xr@gmail.com",
				"password": "somepassword"
			}
		)
		

		user = CustomUser.objects.get(username="xolmumin")		# user bor yo'qligini tekshiradi, yo'q bo'lsa xato qaytadi

		self.assertEqual(user.first_name, "Xolmumin")			# first_name ni borligini tekshiramiz, bor bo'lsa testdan o'tadi
		self.assertEqual(user.last_name, "Abdukarimov")
		self.assertEqual(user.email, "xab60xr@gmail.com")
		self.assertNotEqual(user.password, "somepassword")
		self.assertTrue(user.check_password, ("somepassword"))

	def test_required_fields(self):
		response = self.client.post(
			reverse("users:register"),
			data={
				"first_name": "Xolmumin",
				"email": "xab60xr@gmail.com",
			}
		)

		user_count = CustomUser.objects.count()		# db dagi userlar soni, bu nolga teng bo'lishi kerak

		self.assertEqual(user_count, 0)		# nolga tengligini tekshiramiz
		self.assertFormError(response, "form", "username", "This field is required.")
		self.assertFormError(response, "form", "password", "This field is required.")

	def test_invalid_email(self):		# noto'g'ri email kiritilganini tekshiramiz
		response = self.client.post(
			reverse("users:register"),
			data={
				"username": "xolmumin",
				"first_name": "Xolmumin",
				"last_name": "Abdukarimov",
				"email": "xab60xr-gmail",
				"password": "somepassword"
			}
		)

		user_count = CustomUser.objects.count()		# db dagi userlar soni, bu nolga teng bo'lishi kerak

		self.assertEqual(user_count, 0)		# nolga tengligini tekshiramiz
		# noto'g'ri email kiritilsa nima bo'lishi:
		self.assertFormError(response, "form", "email", "Enter a valid email address.")

	def test_unique_username(self):		# noto'g'ri email kiritilganini tekshiramiz
		# 1. user yaratamiz:
		user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin")
		user.set_password("somepass")
		user.save()

		# 2. bir xil username lik user yaratmoqchimiz:
		response = self.client.post(
			reverse("users:register"),
			data={
				"username": "xolmumin",
				"first_name": "Xolmumin",
				"last_name": "Abdukarimov",
				"email": "xab60xr@gmail.com",
				"password": "somepassword"
			}
		)

		# 3. yaratilgan user bitta bo'lishi kerak:
		user_count = CustomUser.objects.count()
		self.assertEqual(user_count, 1)

		# 4. formada qanday xato chiqishini ko'rsatamiz:
		self.assertFormError(response, "form", "username", "A user with that username already exists.")
		

# login post request uchun test:
class LoginTestCase(TestCase):
	
	def setUp(self):		# har bitta test yurishidan oldin shu funksiya ishlaydi, mana shu funksiya da userni yaratib olamiz, shunda testlarimizda user yaratish kodi takrorlanmaydi. 
		# DRY - Dont repeat yourself
		self.db_user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin")
		self.db_user.set_password("somepass")
		self.db_user.save()


	def test_successful_login(self):
		# # userni bazadan olamiz
		# db_user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin")
		# db_user.set_password("somepass")
		# db_user.save()

		#  userni login qilmoqchimiz:
		self.client.post(
			reverse("users:login"), 	# login url iga post request yuboramiz, va uni ichida data bo'ladi
			data={
				"username": "xolmumin",
				"password": "somepass"		# yani username ham passpowr ham to'g'ri
			}
		)

		# user login bo'lgandan keyin nima bo'lishi kerak:
		# is authentication bo'lishi kerak, buning uchun post yuborayotgan klientni olib olishimiz kerak:
		user = get_user(self.client)

		# userni login qilgan yoki yo'qligini tekshiramiz:
		self.assertTrue(user.is_authenticated)

	# noto'g'ri parol yo username uchun test:
	def test_wrong_credentials(self):
		# db_user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin")
		# db_user.set_password("somepass")
		# db_user.save()

		#  userni login qilmoqchimiz:
		self.client.post(
			reverse("users:login"), # login url iga post request yuboramiz, va uni ichida data bo'ladi
			data={
				"username": "wrong-username",
				"password": "somepass"	# yani username ham passpowr ham to'g'ri
			}
		)

		user = get_user(self.client)
		self.assertFalse(user.is_authenticated)

		#  userni login qilmoqchimiz:
		self.client.post(
			reverse("users:login"), # login url iga post request yuboramiz, va uni ichida data bo'ladi
			data={
				"username": "xolmumin",
				"password": "wrong-password"	# yani username ham passpowr ham to'g'ri
			}
		)

		user = get_user(self.client)
		self.assertFalse(user.is_authenticated)


	# log out uchun test:
	def test_logout(self):
		# db_user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin")
		# db_user.set_password("somepass")
		# db_user.save()

		self.client.login(username="xolmumin", password="somepass")		# login qilamiz

		self.client.get(reverse("users:logout"))		# logout qilish uchun request yuboramiz

		user = get_user(self.client)		# login qilgan user ni olamiz
		self.assertFalse(user.is_authenticated)		# va userni log out qilganini tekshiramiz





# profil page uchun unit test:
class ProfileTestCase(TestCase):
	# login qilmagan user uchun
	def test_login_required(self):
		response = self.client.get(reverse("users:profile"))		# login qilmagan userdan request keladi
		
		# user login page ga yo'naltirildimi?
		# 1- usul: 
		# self.assertEqual(response.url, reverse("users:login"))		# login qilmagan user so'roviga javob url i login page ga teng bo'lishi kerak.
		# ?next=/users/profile/ - bu LoginRequiredMixin clasini qo'shimchasi, buni ham hisobga olib qo'yishimiz kerak.
		self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")
		# 2- usul: redirect ning status kodi orqali tekshiramiz. bizni holda 302 kelishi kerak.
		self.assertEqual(response.status_code, 302)		# status kod 302 ga teng mi ?


	# login bo'lgan userni profile page ida malumotlari paydo bo'lganini tekshiramiz:
	def test_profile_details(self):
		# user yaratamiz:
		user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin", last_name="Abdukarimov", email="xab60xr@gmail.com")
		user.set_password("somepass")
		user.save()

		# endi bu user ni login qilishimiz kerak: 
		# 1-usul: request yuborib qilishimiz mumkin.
		# 2-usul-osonroq: clien.login() funk dan foydalanamiz. o'zi login qilib qo'yadi.
		self.client.login(username="xolmumin", password="somepass")

		# endi profile page ga manashu user dan so'rov yuboramiz:
		response = self.client.get(reverse("users:profile"))

		# status kodini ham tekshirib ko'rsak bo'lladi: bu sucsesfull response bo'lgani uchun uning status kodi 200 ga teng bo'ladi.
		self.assertEqual(response.status_code, 200)

		# endi manashu so'rov ichida(response da) user haqida malumotlar bor yo'qligini tekshiramiz:
		self.assertContains(response, user.username)
		self.assertContains(response, user.first_name)
		self.assertContains(response, user.last_name)
		self.assertContains(response, user.email)

	def test_update_profile(self):
		# user yaratamiz:
		user = CustomUser.objects.create(username="xolmumin", first_name="Xolmumin", last_name="Abdukarimov", email="xab60xr@gmail.com")
		user.set_password("somepass")
		user.save()

		# endi bu user ni login qilishimiz kerak: 
		self.client.login(username="xolmumin", password="somepass")

		# endi profile page ga manashu user dan so'rov yuboramiz:
		response = self.client.post(
			reverse("users:profile-edit"),
				data={
					"username": "xolmumin",
					"first_name": "Xolmumin",
					"last_name": "A",
					"email": "xab60xr@gmail.com"
				}
			)
		user = CustomUser.objects.get(pk=user.pk)	# 1-usul: o'zgargan userni olamiz
		# user.refresh_from_db()	# 2-usul: db dagi ma'lumotlarni yangilab qo'yadi, va userni ishlataversak bo'ladi.
		self.assertEqual(user.last_name, "A")	# last name A ga tengligini, o'zgarganini tekshiramiz
		self.assertEqual(response.url, reverse("users:profile")) # redirekt bo'lganini tekshiramiz
			










