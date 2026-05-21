from django.core import paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Post,Category
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


def index(request):
    return HttpResponse("Hello Django! 这是我的第一个页面")

def post_list(request):
    posts = Post.objects.filter(status='published').select_related('category')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request,'blog/post_list.html',{'page_obj':page_obj})

def post_detail(request,pk):
    post = get_object_or_404(
        Post.objects.select_related('category'),
        pk=pk,
        status='published'
    )
    return render(request,'blog/post_detail.html',{'post':post})

@login_required(login_url='/blog/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 文章创建成功！')
            return redirect('post_list')
        else:
            messages.error(request, '请检查表单中的错误')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})

@login_required(login_url='/blog/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ 文章更新成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form})

@login_required(login_url='/blog/login/')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '🗑️ 文章已删除')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # 注册后自动登录
            messages.success(request, f'👋 欢迎 {user.username}！注册成功！')
            return redirect('post_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


