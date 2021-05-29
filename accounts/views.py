from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import SignUpForm, UserUpdateForm, BloggerUpdateForm, ReaderUpdateForm
from .models import User, Reader, Blogger


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


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	fields = ('first_name', 'last_name', 'email')
	template_name = 'my_account.html'
	success_url = reverse_lazy('my_account')

	def get_object(self):
		return self.request.user


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

		if forms['form'].is_valid():
			forms['form'].save()
			forms['extra'].save()
	else:
		if user.is_blogger:
			extra = BloggerUpdateForm(instance=user.blogger)
		else:
			extra = ReaderUpdateForm(instance=user.reader)

		forms = {'form': UserUpdateForm(instance=user), 'extra': extra}

	return render(request, 'my_account.html', forms)
