from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..views import PostUpdateView


class PostUpdateViewTestCase(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name='TestBoard', description='TestBoard Description')
		self.username = 'testusername'
		self.password = 'testpassword123'
		user = User.objects.create_user(username=self.username, email='test@email.com', password=self.password)
		self.topic = Topic.objects.create(subject='TestSubject', board=self.board, starter=user)
		self.post = Post.objects.create(message='TestMessage', topic=self.topic, created_by=user)
		self.url = reverse('edit_post', kwargs={
			'pk': self.board.pk,
			'topic_pk': self.topic.pk,
			'post_pk': self.post.pk
		})


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
	def test_redirection(self):
		login_url = reverse('login')
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
	def setUp(self):
		super().setUp()

		username = 'testname'
		password = 'testpass123'

		user = User.objects.create_user(username=username, email='test@mail.com', password=password)
		self.client.login(username=username, password=password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 404)
