from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from venv import create
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
# from matplotlib.style import context


from users.forms import UserCreateForm, UserUpdateForm	#, UserLoginForm


# Create your views here.
class RegisterView(View):
	def get(self, request):
		create_form = UserCreateForm()
		context = {"form": create_form}
		return render(request, "users/register.html", context)
	
	def post(self, request):		# malumotlarni qabul qilib olish
		create_form = UserCreateForm(data=request.POST) 	# validatsiya uchun formani chaqirish

		if create_form.is_valid():		# validatsiya qiladi
			create_form.save()		# forms.py dagi  metodni chaqiramiz pastdagi kodning o'rniga
			# username = request.POST['username']
			# first_name = request.POST['first_name']
			# last_name = request.POST['last_name']
			# email = request.POST['email']
			# password = request.POST['password']

			# user = User.objects.create(		# user obyek yatatib, kiritilgan qiymatlarni db ga qo'shadi:
			# 	username = username,
			# 	first_name = first_name,
			# 	last_name = last_name,
			# 	email = email
			# )
			# user.set_password(password)			# password ni hash ga aylantirib yuborish
			# user.save()

			# create user account
			return redirect('users:login')
		else:		# xato bo'ksa qanaqa xatoligini ko'rsatadi
			context = {"form": create_form}
			return render(request, "users/register.html", context)


class LoginView(View):
	def get(self, request):
		login_form = AuthenticationForm()

		return render(request, "users/login.html", {"login_form": login_form})
	
	def post(self, request):
		# print(request.POST['username'], request.POST['password'])
		login_form = AuthenticationForm(data=request.POST)	# data ni postga berib yuboramiz

		# formani to'g'rimi yo'qligini tekshiramiz:
		if login_form.is_valid():
			# userni login qilamiz va userga sessiya ochamiz
			user = login_form.get_user()
			login(request, user)
			messages.success(request, "Siz saxifaga muvafaqiyatli kirdingiz!")	
			return redirect("books:list")
		else:
			return render(request, "users/login.html", {"login_form": login_form})


class ProfileView(LoginRequiredMixin, View):
	def get(self, request):		# user ni request ichidan olamiz.

		# ------------ bu qisimning vazifasini django ni classi LoginRequiredMixein bajaradi ------------------

		# if not request.user.is_authenticated:		# agar user login qilmagan bo'lsa uni login page ga yo'naltirib yuboramiz.
		# 	return redirect("users:login")
		# -------------------------------------------------------------------------------------------------------

		return render(request, "users/profile.html", {"user": request.user})		# html saxifaga yo'naltiramiz. va manashu requestni yuborgan(login qilgan yo qilmagan) userni uzatamiz


class LogoutView(LoginRequiredMixin, View):		# faqat login qilganlar uchun.
	def get(self, request):
		logout(request)		# log out qilib beradi
		messages.info(request, "Siz saxifangizdan muvafaqiyatli chiqdingiz.")		# malumot chiqarish uchun, xabar yaratamiz. faqat bir martalik xabar. 
		# messages.warning()
		# messages.error()		# xato bo'lsa
		# messages.success()		# muvafaqiyatli bajarilsa
		return redirect("landing_page")


class ProfileUpdateView(LoginRequiredMixin, View):
	def get(self, request):
		user_update_form = UserUpdateForm(instance=request.user)
		return render(request, "users/profile_edit.html", {"form": user_update_form})

	def post(self, request):
		user_update_form = UserUpdateForm(
										instance=request.user,
										data=request.POST,
										files=request.FILES
										)

		if user_update_form.is_valid():
			user_update_form.save()
			messages.success(request, "You have succesfully updated your profile.")

			return redirect("users:profile")
		
		return render(request, "users/profile_edit.html", {"form": user_update_form})



