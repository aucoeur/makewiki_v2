from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from wiki.models import Page
from wiki.forms import PageForm


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
          'page': page
        })

class PageNewView(FormView):
  """ Renders a Create New Page Form """
  template = 'new_page.html'
  form_class = PageForm
  success_url = '' 

  def get(self, request):
    form = PageForm()
    return render(request, 'new_page.html', {'form': form})
  
  def post(self, request):
    if request.method == 'POST':
      form = PageForm(request.POST)
      if form.is_valid():
        article = form.save()
        return HttpResponseRedirect(reverse_lazy('wiki-details-page', args = [article.slug]))
      return render(request, 'new_page.html', {'form': form})