from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('books:index') # переход на страницу, после авторизации

			return render(request, 'loginsys/login_user.html', {
				'error_message': 'Ваш аккаунт был деактивирован'
				})
		else:
			return render(request, 'loginsys/login.html', {
				'error_message': 'Неправильный логин или пароль. Попробуйте заново'
				})
	return render(request, 'loginsys/login.html')

def logout_user(request):
	logout(request)
	# form = UserForm(request.POST)
	# return render(request, 'loginsys/login.html', {'form': form})
	return redirect('loginsys:login_user')

def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user.is_active:
			login(request, user)
			return redirect('books:index')
		return render(request, 'loginsys/login_user.html', {
				'error_message': 'Ваш аккаунт был деактивирован'
				})
	return render(request, 'loginsys/register.html', {'form': form})