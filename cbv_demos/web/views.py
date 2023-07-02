from django import forms
from django.forms import modelform_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from cbv_demos.web.models import Article

class BaseView:
    def get(self, request):
        pass

    def post(self, request):
        pass

    @classmethod
    def as_view(cls):
        self = cls()

        def view(request):
            if request.method == 'GET':
                return self.get(request)
            else:
                return self.post(request)

        return view

def list_articles(request):
    context={
        'articles': Article.objects.all(),
    }
    return render(request, 'list.html', context)

class ArticleListView(views.ListView):


    template_name='list.html'
    model=Article
    context_object_name='articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', '')
        queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['search']=self.request.GET.get('search', '')
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     search = self.request.GET.get('search', '')
    #     queryset = queryset.filter(title__icontains=search)
    #     return queryset
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['search'] = self.request.GET.get('search', '')
    #     return context
# class ArticleListView(views.View):
#     def get(self):
#         context={
#             'articles':Article.objects.all(),
#         }
#
#
#         return render(self.request, 'list.html', context)

class DisabledFormFieldsMixin:
    disabled_fields = ()

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # fields = self.disabled_fields \
        # if self.disabled_fields != '__all__' \
        # else

        for field in self.disabled_fields:
            form.fields[field].widget.attrs['disabled'] = 'disabled'
            form.fields[field].widget.attrs['readonly'] = 'readonly'

        return form


class ArticleDetailView(views.DetailView):
    model =Article
    template_name = 'detail.html'

class ArticleCreateView(DisabledFormFieldsMixin, views.CreateView):
    model=Article
    template_name = 'create.html'
    fields = '__all__'
    success_url = reverse_lazy('list_articles_cbv')
    disabled_fields = ('title',)

class ArticleDeleteView(DisabledFormFieldsMixin, views.DeleteView):
    model = Article
    template_name = 'delete.html'
    form_class = modelform_factory(
        Article,
        fields=('title', 'content')
    )

    disabled_fields = ('title', 'content')

    def get_form_kwargs(self):
        instance = self.get_object()
        form_kwargs = super().get_form_kwargs()

        form_kwargs.update(instance=instance)
        return form_kwargs

class RedirectToArticlesView(views.RedirectView):
    url = reverse_lazy('list_articles_cbv')