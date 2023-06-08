from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

from posts.models import Post,Category

# Create your views here.
def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE)
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
    }

    return render(request, 'frontpage.html', context)

def about(request):
    return render(request, 'about.html')

def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")