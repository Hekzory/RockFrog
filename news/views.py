from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Post
from django.http import HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class NewsListView(View):
    def get(self, request):
        page = self.request.GET.get('page')
        allarticles = Post.objects.all()[::-1]
        paginator = Paginator(allarticles, 4)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            articles = paginator.page(paginator.num_pages)

        template = loader.get_template('news/index.html')
        context = {
            'articles': articles,
        }
        return HttpResponse(template.render(context, request))


def news_post(request, news_id):
    #post = Post.objects.get(pk=news_id)
    post = get_object_or_404(Post, pk=news_id)
    template = loader.get_template('news/posttemplate.html')
    context = {
        'post': post,
    }
    return HttpResponse(template.render(context, request))
