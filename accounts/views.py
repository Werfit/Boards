from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserUpdateForm, BloggerUpdateForm, ReaderUpdateForm
from .models import User


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save()

			auth_login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {
		'form': form
	})


@login_required
def update_profile(request):
	user = User.objects.get(id=request.user.id)

	if request.method == 'POST':
		if user.is_blogger:
			extra = BloggerUpdateForm(request.POST, instance=user.blogger)
		else:
			extra = ReaderUpdateForm(request.POST, instance=user.reader)

		forms = {
			'form': UserUpdateForm(request.POST, instance=user),
			'extra': extra
		}

		if forms['form'].is_valid() and forms['extra'].is_valid():
			forms['form'].save()
			forms['extra'].save()
			messages.success('Your account was updated successfully')
	else:
		if user.is_blogger:
			extra = BloggerUpdateForm(instance=user.blogger)
		else:
			extra = ReaderUpdateForm(instance=user.reader)

		forms = {'form': UserUpdateForm(instance=user), 'extra': extra}

	return render(request, 'my_account.html', forms)
