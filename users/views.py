from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from venv import create
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View


from users.forms import UserCreateForm, UserUpdateForm


class RegisterView(View):
	def get(self, request):
		create_form = UserCreateForm()
		context = {"form": create_form}
		return render(request, "users/register.html", context)
	
	def post(self, request):
		create_form = UserCreateForm(data=request.POST)

		if create_form.is_valid():
			create_form.save()
			
			# create user account
			return redirect('users:login')
		else:
			context = {"form": create_form}
			return render(request, "users/register.html", context)


class LoginView(View):
	def get(self, request):
		login_form = AuthenticationForm()

		return render(request, "users/login.html", {"login_form": login_form})
	
	def post(self, request):
		login_form = AuthenticationForm(data=request.POST)

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
	def get(self, request):
		return render(request, "users/profile.html", {"user": request.user})


class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.info(request, "Siz saxifangizdan muvafaqiyatli chiqdingiz.")
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