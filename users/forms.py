from django.core.mail import send_mail
from django import forms
# from django.contrib.auth.models import User
from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

	def save(self, commit=True):		# passwordni hash ko'rinishida saqlaydi
		user = super().save(commit)
		user.set_password(self.cleaned_data['password'])
		user.save()

		# registratsiya muvafaqiyatli bo'lganligi to'g'risida email xabar yuborish:
		if user.email:
			send_mail(
				'Welcome to Goodreads Clone',
				f"Hi, {user.username}. Welcome to Goodreads Clone. Enjoy the books and reviews.",
				'xab60xr@gmail.com',
				[user.email]
			)

		return user


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('username', 'first_name', 'last_name', 'email', "profile_picture")

		

# class UserCreateForm(forms.Form):
# 	username = forms.CharField(max_length=150)
# 	email = forms.EmailField()
# 	first_name = forms.CharField(max_length=150)
# 	last_name = forms.CharField(max_length=150)
	# password = forms.CharField(max_length=128)

# 	def save(self):
# 		username = self.cleaned_data['username']
# 		first_name = self.cleaned_data['first_name']
# 		last_name = self.cleaned_data['last_name']
# 		email = self.cleaned_data['email']
# 		password = self.cleaned_data['password']

# 		user = User.objects.create(		# user obyek yatatib, kiritilgan qiymatlarni db ga qo'shadi:
# 			username = username,
# 			first_name = first_name,
# 			last_name = last_name,
# 			email = email
# 		)
# 		user.set_password(password)			# password ni hash ga aylantirib yuborish
# 		user.save()

# 		return user


# class UserLoginForm(forms.Form):
# 	username = forms.CharField(max_length=150)
# 	password = forms.CharField(max_length=128)
