from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy

from .forms import AddPostForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}
        ]


class MenHome(ListView):
    model = Men
    template_name = 'celebrities/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Men.objects.filter(is_published=True)


# def index(request):
#     posts = Men.objects.all()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Главная страница',
#                'cat_selected': 0
#                }
#     return render(request, 'celebrities/index.html', context=context)


def about(request):
    return render(request, 'celebrities/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'celebrities/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'celebrities/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Men
    template_name = 'celebrities/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Men, slug=post_slug)
#
#     context = {'post': post,
#                'menu': menu,
#                'title': post.title,
#                'cat_selected': post.cat_id
#                }
#     return render(request, 'celebrities/post.html', context=context)


class MenCategory(ListView):
    model = Men
    template_name = 'celebrities/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


# def show_category(request, cat_slug):
#     cat_id = Category.objects.get(slug=cat_slug).pk
#     posts = Men.objects.filter(cat_id=cat_id)
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Главная страница',
#                'cat_selected': cat_id
#                }
#     if len(posts) == 0:
#         raise Http404
#     return render(request, 'celebrities/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
