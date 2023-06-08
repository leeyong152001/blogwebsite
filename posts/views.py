from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from django.contrib.auth import get_user_model
from .audio import loadAudio
import threading
import time


User = get_user_model()

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    post.click = post.click + 1
    post.save()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail',category_slug, slug)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {'post': post,'category': category_slug , 'form': form })

def like(request,category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    post.like = post.like + 1
    post.save()
    return redirect('post_detail',category_slug, slug)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'category.html', {'category': category, 'posts': posts})

def search(request):
    query = request.GET.get('query','')
    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))
    categories = Category.objects.all()

    object_list = {}
    for post in posts:
        object_list[post] = {
            'title': post.title,
            'slug': post.slug,
            'created_at': post.created_at,
            'intro': post.intro,
            'image': post.image,
            'categories':categories,
        }

    context = {
        'object_list': object_list,
        'query':query,
    }

    return render(request, 'search.html', context)

def add_category(request):
    if request.method =="POST":
        title = request.POST['title']
        slug = request.POST['slug']
        if (Category.objects.filter(title=title)):
            messages.info(request,"Da co")
        else:
            category = Category(title=title,slug=slug)
            category.save()
            messages.info(request, "Da them thanh cong")

    categories = Category.objects.all()
    context = {
        "categories": categories
    }

    return render(request,'dash_category.html',context)

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    context = {
        "category":category,
        "categories": categories
    }
    return render(request,'dash_category.html',context)

def update_category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    category.title = request.POST['title']
    category.slug = request.POST['slug']
    category.save()

    messages.info(request, "Da sua thanh cong")

    return redirect("add_category")

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    messages.info(request, "Da xoa thanh cong")

    return redirect("add_category")

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            auth = Author.objects.filter(user=request.user)
            post.author = auth[0]
            post.save()

            category = Category.objects.filter(id=request.POST['categories'])
            post.categories.set(category)
            post.save()

            try:
                loadAudio(post.body, post.title)
            except:
                ...
            
            messages.info(request, f"Đăng thành công.")
            return redirect('add_post')
    else:
        form = PostForm()

    posts = Post.objects.all()
    context = {
        'posts':posts,
        'form':form
    }

    return render(request,'dash_post.html',context)

def edit_post(request,slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.all()
    context = {
        "post":post,
        "categories": categories
    }
    return render(request,'dash_post.html',context)

def update_post(request,slug):
    post = get_object_or_404(Post, slug=slug)
    post.title = request.POST['title']
    post.intro = request.POST['intro']
    post.body = request.POST['body']
    post.status  = request.POST['status']
    category = Category.objects.filter(title = request.POST['category'])
    post.categories.set(category)
    post.save()
    messages.info(request, 'Đã sửa xong')

    return redirect("dash_base")

def delete_post(request,slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    messages.info(request, "Da xoa thanh cong")

    return redirect("dash_base")

def chart():
    import matplotlib.pyplot as plt
    import os
    posts = Post.objects.filter(status=Post.ACTIVE)

    x = []
    y = []
    for post in posts:
        x.append(post.title)
        y.append(post.click)
    plt.bar(x, y)
    savepath = os.path.join('./core/static/img', 'chart.png')
    plt.savefig(savepath)

def dash_base(request):
    categories = Category.objects.all()
    if (request.user.username == "admin"):
        posts = Post.objects.all()
    else:
        author = Author.objects.filter(user = request.user)
        posts = Post.objects.filter(author= author[0])
    try:
        chart()
    except:
        ...
    context = {
        "categories":categories,
        "posts": posts
    }
    return render(request,'dash_base.html',context)