from django.urls import reverse, resolve
from django.test import TestCase

from ..models import Board
from ..views import TopicListView


class BoardTopicsTest(TestCase):
	def setUp(self):
		Board.objects.create(name='TestTopicName', description='TestTopicName board')

	def test_board_topics_view_success_status_code(self):
		url = reverse('board_topics', kwargs={
			'pk': 1
		})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_board_topics_view_not_found_statuc_code(self):
		url = reverse('board_topics', kwargs={
			'pk': 99
		})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_board_topics_url_resolves_board_topics_view(self):
		view = resolve('/boards/1/')
		self.assertEquals(view.func.view_class, TopicListView)

	def test_board_topics_view_contains_navigation_links(self):
		board_topics_url = reverse('board_topics', kwargs={
			'pk': 1
		})
		response = self.client.get(board_topics_url)
		homepage_url = reverse('home')
		new_topic_url = reverse('new_topic', kwargs={
			'pk': 1
		})

		self.assertContains(response, f'href="{homepage_url}"')
		self.assertContains(response, f'href="{new_topic_url}"')


