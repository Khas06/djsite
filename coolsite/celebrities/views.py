from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .forms import AddPostForm
from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}
        ]


def index(request):
    posts = Men.objects.all()
    context = {'posts': posts,
               'menu': menu,
               'title': 'Главная страница',
               'cat_selected': 0
               }
    return render(request, 'celebrities/index.html', context=context)


def about(request):
    return render(request, 'celebrities/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'celebrities/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Men, slug=post_slug)

    context = {'post': post,
               'menu': menu,
               'title': post.title,
               'cat_selected': post.cat_id
               }
    return render(request, 'celebrities/post.html', context=context)


def show_category(request, cat_slug):
    cat_id = Category.objects.get(slug=cat_slug).pk
    posts = Men.objects.filter(cat_id=cat_id)
    context = {'posts': posts,
               'menu': menu,
               'title': 'Главная страница',
               'cat_selected': cat_id
               }
    if len(posts) == 0:
        raise Http404
    return render(request, 'celebrities/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
