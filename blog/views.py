from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Blog, Comment
from django.db.models import Q
# from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from taggit.models import Tag


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    blogs = Blog.objects.filter(tags=tag)

    return render(request, 'blog/tagged.html', {
        'tag': tag,
        'blogs': blogs
    })

class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'blog'
    template_name = 'blog/blog_list.html'


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    tags = blog.tags.all()
    comments = blog.comments.all()
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.blog = blog
                new_comment.user = request.user
                new_comment.save()
                return redirect('blog:blog_detail', slug=slug)
        else:
            return redirect('login')
    else:
        comment_form = CommentForm()

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'tags': tags,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog:blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('blog:blog_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('login')



# def search(request):
#     query = request.GET.get('q')
#     if query:
#         search_vector = SearchVector('title', 'content', config='english')
#         search_query = SearchQuery(query)
#         blogs = Blog.objects.annotate(
#             search=search_vector,
#             rank=SearchRank(search_vector, search_query),
#             trigram=TrigramSimilarity('title', query),
#         ).filter(Q(rank__gte=0.3) | Q(trigram__gt=0.1)).order_by('-rank', '-trigram')
#     else:
#         blogs = Blog.objects.none()
#     return render(request, 'blog/search_results.html', {'blogs': blogs, 'query': query})

2

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog:blog_detail', slug=comment.blog.slug)