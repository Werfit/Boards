from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import PostListView
from ..models import Board, Post, Topic


class TopicPostsTests(TestCase):
	def setUp(self):
		board = Board.objects.create(name='TestBoard', description='TestBoard Description')
		user = User.objects.create_user(username='testuser', email='test@mail.com', password='testpassword123')
		topic = Topic.objects.create(subject='TestSubject', board=board, starter=user)
		Post.objects.create(message='TestPost Message', topic=topic, created_by=user)

		url = reverse('topic_posts', kwargs={
			'pk': board.pk,
			'topic_pk': topic.pk
		})
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/boards/1/topics/1/')
		self.assertEquals(view.func.view_class, PostListView)
