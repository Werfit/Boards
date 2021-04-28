from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name='TestBoard', description='TestBoard Description')
		self.username = 'testusername'
		self.password = 'testpassword123'
		user = User.objects.create_user(username=self.username, email='test@email.com', password=self.password)
		self.topic = Topic.objects.create(subject='TestSubject', board=self.board, starter=user)
		Post.objects.create(message='TestMessage', topic=self.topic)
		self.url = reverse('reply_topic', kwargs={
			'pk': self.board.pk,
			'topic_pk': self.topic.pk
		})

