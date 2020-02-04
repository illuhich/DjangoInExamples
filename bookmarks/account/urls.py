from django.urls import path
# from django.contrib.auth.views import LoginView
from . import views

app_name = 'account'

urlpatterns = [
	# path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
	path('login/', views.user_login, name='login')
]