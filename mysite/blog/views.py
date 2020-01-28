from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView


# def post_list(request):
# 	# posts = Post.objects.filter(status='published')
# 	object_list = Post.objects.all()
# 	paginator = Paginator(object_list, 3)
# 	page = request.GET.get('page')
# 	try:
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 		# if page is not an integer deliver the first page
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 		# if page is out of range deliver the last page of results
# 		posts =  paginator.page(paginator.num_pages)
# 	context = {'posts': posts, 'page': page}
# 	return render(request, 'post/list.html', context)

class PostListView(ListView):
	queryset = Post.objects.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'post/list.html'


def post_detail(request, year, month, day, post):
	# post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
	post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
	return render(request, 'post/detail.html', {'post':post})
