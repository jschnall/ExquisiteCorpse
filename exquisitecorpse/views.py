__author__ = 'jschnall'

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import View, CreateView, DeleteView, UpdateView

import json

from api.models import *
from forms import *
from mixins import *

class IndexView(TemplateView):
    template_name = 'exquisitecorpse/index.html'

    def get_context_data(self, **kwargs):
        latest_compositions = Composition.objects.filter(completed__isnull=False).order_by('-completed')[:5]
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest_compositions'] = latest_compositions
        return context


class CompositionList(ListView):
    queryset = Composition.objects.order_by('-updated')
    template_name = 'exquisitecorpse/composition_list.html'
    context_object_name = 'compositions'
    paginate_by = settings.EXQUISITE_CORPSE['PAGINATE_BY']
    nav_size = settings.EXQUISITE_CORPSE['NAV_PAGINATE_BY']

    def get_context_data(self, **kwargs):
        paginator, page, object_list, is_paginated = self.paginate_queryset(self.queryset, self.paginate_by)
        nav_paginator = Paginator(range(1, paginator.num_pages + 1), self.nav_size)
        page_nums = nav_paginator.page(1 + (page.number-1) // self.nav_size)

        context = super(CompositionList, self).get_context_data(**kwargs)
        context['page_nums'] = page_nums
        return context


class AvailableCompositionList(CompositionList):
    def get_queryset(self):
        return Composition.objects.filter(Q(start_time__isnull=True) | Q(start_time__gt=timezone.now())).order_by('-updated')


class CompletedCompositionList(CompositionList):
    def get_queryset(self):
        return Composition.objects.filter(completed__isnull=False).order_by('-completed')


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'exquisitecorpse/dashboard.html'
    context_object_name = 'compositions'

    QUEUED = 'queued'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    FAVORITES = 'favorites'
    CATEGORY_CHOICES = (
        (QUEUED, 'Queued'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (FAVORITES, 'Favorites'),
    )

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['queued_count'] = Composition.objects.filter(users=self.request.user).filter(Q(start_time__isnull=True) | Q(start_time__gt=timezone.now())).count()
        context['active_count'] = Composition.objects.filter(users=self.request.user, start_time__gt=timezone.now(), completed__isnull=True).count()
        context['completed_count'] = Composition.objects.filter(users=self.request.user, completed__isnull=False).count()
        context['favorite_count'] = Composition.objects.filter(favorites=self.request.user).count()
        return context

    def get_queryset(self):
        category = self.kwargs.get('category', None)

        if category == self.QUEUED:
            return Composition.objects.filter(users=self.request.user).filter(Q(start_time__isnull=True) | Q(start_time__gt=timezone.now())).order_by('-updated')
        elif category == self.ACTIVE:
            return Composition.objects.filter(users=self.request.user, start_time__gt=timezone.now(), completed__isnull=True).order_by('-updated')
        elif category == self.COMPLETED:
            return Composition.objects.filter(users=self.request.user, completed__isnull=False).order_by('-completed')
        elif category == self.FAVORITES:
            return Composition.objects.filter(favorites=self.request.user).order_by('-updated')


class CompositionDetails(DetailView):
    model = Composition
    template_name = 'exquisitecorpse/composition_details.html'


class CompositionCreate(LoginRequiredMixin, CreateView):
    model = Composition
    template_name = 'exquisitecorpse/composition_create.html'
    form_class = CompositionForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.active_user = self.request.user
        response = super(CompositionCreate, self).form_valid(form)
        form.instance.users.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy('corpse:composition_details', args=(self.object.pk,))


class CompositionUpdate(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Composition
    template_name = 'exquisitecorpse/composition_create.html'
    form_class = CompositionForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super(CompositionCreate, self).form_valid(form)
        form.instance.users.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy('corpse:composition_details', args=(self.object.pk,))


class ToggleUserM2MFieldView(LoginRequiredMixin, AjaxableResponseMixin, View):
    '''
    Toggles the current user in an M2M field
    '''

    def post(self, request):
        try:
            pk = request.POST['pk']
            obj = self.model.objects.get(pk=pk)
            m2m_field = getattr(obj, self.field)
            exists = request.user in m2m_field.all()
            if exists:
                m2m_field.remove(request.user)
            else:
                m2m_field.add(request.user)
            return JsonResponse({'count': m2m_field.count(), 'exists': not exists})
        except:
            raise ImproperlyConfigured('Valid "model" and M2M "field" are required.')


class CompositionLike(ToggleUserM2MFieldView):
    model = Composition
    field = 'likes'


class CompositionFavorite(ToggleUserM2MFieldView):
    model = Composition
    field = 'favorites'


class CompositionDelete(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = Composition
    success_url = reverse_lazy('composition_list')
    #template_name = 'exquisitecorpse/composition_delete.html'


class PartDetails(DetailView):
    model = Part
    #template_name = 'exquisitecorpse/part_details.html'


class PartCreate(CreateView):
    model = Part
    #template_name = 'exquisitecorpse/part_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PartCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('corpse:part_details', args=(self.object.pk,))


class PartLike(ToggleUserM2MFieldView):
    model = Part
    field = 'likes'
