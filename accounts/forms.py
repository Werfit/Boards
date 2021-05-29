from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Reader, Blogger, CHOICES
from .widgets import DateInput


class SignUpForm(UserCreationForm):
    ROLES = (
        (1, 'Blogger'),
        (2, 'Reader')
    )

    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    role = forms.ChoiceField(widget=forms.RadioSelect(), choices=ROLES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        if commit:
            user.save()

            if role == '1':
                user.is_blogger = True
                Blogger.objects.create(user=user)
            elif role == '2':
                user.is_reader = True
                Reader.objects.create(user=user)

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class BloggerUpdateForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(choices=CHOICES)

    class Meta:
        model = Blogger
        fields = ('categories', 'country', 'birthday')
        widgets = {
            'birthday': DateInput
        }


class ReaderUpdateForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(choices=CHOICES)

    class Meta:
        model = Reader
        fields = ('interests', 'is_adult')
