from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
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
    return HttpResponse("Добавить статью")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def show_category(request, cat_id):
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
