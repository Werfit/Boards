from django import forms
from .models import Board, Topic, Post


class NewBoardForm(forms.ModelForm):
	class Meta:
		model = Board
		fields = ('name', 'description')


class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
		),
		max_length=4000,
		help_text='The max length of the text 4000.'
	)

	class Meta:
		model = Topic
		fields = ('subject', 'message')


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('message',)
