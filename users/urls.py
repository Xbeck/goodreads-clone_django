from django.urls import path

from users.views import LoginView, RegisterView, ProfileView, LogoutView, ProfileUpdateView

app_name = 'users'
urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('profile/', ProfileView.as_view(), name='profile'),		# view dagi userni urlga ulaymiz
	path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]