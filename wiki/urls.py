from django.urls import path
from wiki.views import PageListView, PageDetailView, PageNewView
from wiki.forms import PageForm


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    path('new', PageNewView.as_view(), name='new-page')
]
