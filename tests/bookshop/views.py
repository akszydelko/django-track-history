import json

from django.forms import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from .models import Author


class IndexView(TemplateView):
    template_name = 'index.html'


class AuthorCreateView(CreateView):
    model = Author
    fields = ['name', 'genre']

    def form_valid(self, form):
        self.object = form.save()
        response = {
            'status': 'OK',
            'object': model_to_dict(self.object)
        }
        return HttpResponse(json.dumps(response), status=201, content_type='application/json')

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')


class AuthorDetailView(DetailView):
    model = Author

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponse(json.dumps(model_to_dict(self.object)), status=200, content_type='application/json')


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['genre']

    def form_valid(self, form):
        self.object = form.save()
        response = {
            'status': 'OK',
            'object': model_to_dict(self.object)
        }
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
