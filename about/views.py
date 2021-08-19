from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthor(TemplateView):
    template_name = 'about_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['text'] = 'Я автор: https://github.com/dyachkov-pavel'
        return context


class AboutTech(TemplateView):
    template_name = 'technology.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['text'] = 'Ноутбук, интернет, python, django'
        return context


class AboutFoodgram(TemplateView):
    template_name = 'foodgram.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продуктовый помощник'
        context['text'] = ('«Продуктовый помощник» - это онлайн сервис,'
                           'где пользователи смогут публиковать рецепты,'
                           'подписываться на публикации других пользователей,'
                           'добавлять понравившиеся рецепты в'
                           'список «Избранное», а перед походом в '
                           'магазин скачивать сводный список'
                           'продуктов, необходимых для приготовления '
                           'одного или нескольких выбранных блюд')
        return context
