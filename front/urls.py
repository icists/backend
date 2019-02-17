# front/urls
from django.urls import path

from . import views

"""
- path() returns an element for inclusion in urlspatterns.

@params
- route: a string that contains url pattern
    The string may contain angle brackets(e.g. <username>) to sent it as a arg to the view.
- view: a view functino or the result of as_view() (this is for class based views)
    or it can be an django.urls.include()
- kwargs: to pass additional arguments to the view function or method.
"""
urlpatterns = [
    path('', views.index, name='index')
]