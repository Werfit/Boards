from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

from accounts.decorators import blogger_required

from .forms import NewBoardForm, NewTopicForm, PostForm
from .models import Board, Topic, Post


class HomeView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'index.html'
	paginate_by = 5


class TopicListView(ListView):
	model = Topic
	context_object_name = 'topics'
	template_name = 'topics.html'
	paginate_by = 20

	def get_context_data(self, **kwargs):
		kwargs['board'] = self.board
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.board = get_object_or_404(Board, pk=self.kwargs['pk'])
		queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
		return queryset


class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'topic_posts.html'
	paginate_by = 2

	def get_context_data(self, **kwargs):
		session_key = f'viewed_topic_{self.topic.pk}'
		if not self.request.session.get(session_key, False):
			self.topic.views += 1
			self.topic.save()
			self.request.session[session_key] = True

		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
		queryset = self.topic.posts.order_by('created_at')
		return queryset


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
	model = Post
	fields = ('message',)
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()

		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@method_decorator(login_required, name='dispatch')
@method_decorator(blogger_required, name='dispatch')
class BoardUpdateView(UpdateView):
	model = Board
	fields = ('name', 'description')
	template_name = 'edit_board.html'
	pk_url_kwarg = 'board_pk'
	context_object_name = 'board'

	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'The board was successfully updated')
		return redirect('home')


@login_required
@blogger_required
def new_board(request):
	if request.method == 'POST':
		form = NewBoardForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Your board was successfully created!')

			return redirect('home')
	else:
		form = NewBoardForm()

	return render(request, 'new_board.html', {
		'form': form
	})


@login_required
def new_topic(request, pk=None):
	board = get_object_or_404(Board, pk=pk)

	if request.method == 'POST':
		form = NewTopicForm(request.POST)

		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()

			Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=request.user
			)

			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()

	return render(request, 'new_topic.html', {
		'board': board,
		'form': form
	})


@login_required
def reply_topic(request, pk=None, topic_pk=None):
	topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = request.user
			post.save()

			topic.last_updated = timezone.now()
			topic.save()

			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
	else:
		form = PostForm()
	return render(request, 'reply_topic.html', {
		'topic': topic,
		'form': form
	})


@login_required
@blogger_required
def delete_board(request, pk=None):
	board = get_object_or_404(Board, pk=pk)
	data = {}

	if request.method == 'POST':
		messages.success(request, 'The board was successfully deleted')
		board.delete()
		data['form_is_valid'] = True
		boards = Board.objects.all()

		paginator = Paginator(boards, 5)
		paginated_boards = paginator.page(request.GET.get('page'))

		data['html_board_list'] = render_to_string('includes/boards.html', {
			'boards': paginated_boards,
			'user': request.user,
			'page_obj': {'number': request.GET.get('page')}
		}, request=request)

	return JsonResponse(data)
