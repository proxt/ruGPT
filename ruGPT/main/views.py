from django.shortcuts import render
from .models import Articles
from django.views.generic import DetailView


def index(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'main/index.html', {'title': 'Главная', 'news': news})


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'main/details_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context





def about(request):
    return render(request, 'main/abo    ut.html', {'title': 'О нас'})

