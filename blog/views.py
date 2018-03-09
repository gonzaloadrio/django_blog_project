from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

def post_list(request):

    page_size = 5
    try:
        page_size = int(request.GET.get('size'))
    except:
        pass


    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts_list, page_size) # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        if int(page) <= 0 :
            return redirect('/?page=1')
        elif int(page) > paginator.num_pages :
            return redirect('/?page='+ paginator.num_pages.__str__())
        else:
            posts = paginator.page(page)
            return render(request, 'blog/post_list.html', {'posts': posts})
    except (ValueError, PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        return redirect('/?page=1')
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return redirect('/?page=' + paginator.num_pages.__str__())


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
