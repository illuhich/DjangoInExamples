from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, EmailPostForm2, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet


def post_list(request, tag_slug=None):
	# posts = Post.objects.filter(status='published')
	object_list = Post.objects.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = Post.objects.filter(tags__in=[tag])

	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# if page is out of range deliver the last page of results
		posts =  paginator.page(paginator.num_pages)
	context = {'posts': posts, 'page': page, 'tag': tag}
	return render(request, 'post/list.html', context)

# class PostListView(ListView):
# 	queryset = Post.objects.all()
# 	context_object_name = 'posts'
# 	paginate_by = 3
# 	template_name = 'post/list.html'


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
	comments = post.comments.filter(active=True)
	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to database
			new_comment.save()
	else:
		comment_form = CommentForm()
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
	context = {'post':post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts}
	return render(request, 'post/detail.html', context)


def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		# Form was submitted
		form = EmailPostForm(request.POST)
		form2 = EmailPostForm2(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com',[cd['to']])
			sent = True
			#  ... send mail
		elif form2.is_valid():
			cd = form2.cleaned_data
			subject = 'Рассылка FoxyShop'
			message = 'Подписка на рассылку прошла успешно!'
			send_mail(subject, message, 'admin@myblog.com',[cd['email']])
			sent = True
	else:
		form = EmailPostForm()
		form2 = EmailPostForm2()
	context = {'post': post, 'form': form, 'form2': form2,'sent': sent}
	return render(request, 'post/share.html', context)


def post_search(request):
	form = SearchForm()
	cd = None
	results = None
	total_results = None
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
			total_results = results.count()
	context = {'form': form, 'cd': cd, 'results': results, 'total_results': total_results}
	return render(request, 'post/search.html', context)

