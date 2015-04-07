__author__ = 'jschnall'

from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from api.models import *
from forms import *
from mixins import *

def index(request):
    latest_compositions = Composition.objects.filter(completed__isnull=False).order_by('-completed')[:5]
    context = {'latest_compositions': latest_compositions}
    return render(request, 'exquisitecorpse/index.html', context)


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
        return Composition.objects.filter(started__isnull=True).order_by('-updated')


class CompletedCompositionList(CompositionList):
    def get_queryset(self):
        return Composition.objects.filter(completed__isnull=False).order_by('-completed')


class UserQueuedCompositionList(CompositionList):
    def get_queryset(self):
        return Composition.objects.filter(users=self.request.user, started__isnull=True).order_by('-updated')


class UserActiveCompositionList(CompositionList):
    def get_queryset(self):
        return Composition.objects.filter(users=self.request.user, started__isnull=False, completed__isnull=True).order_by('-updated')


class UserCompletedCompositionList(CompositionList):
        def get_queryset(self):
            return Composition.objects.filter(users=self.request.user, completed__isnull=False).order_by('-completed')


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'exquisitecorpse/dashboard.html'
    context_object_name = 'my_compositions'

    def get_queryset(self):
        return Composition.objects.filter(users=self.request.user).order_by('-updated')


class CompositionDetails(DetailView):
    model = Composition
    template_name = 'exquisitecorpse/composition_details.html'


class CompositionCreate(AjaxableResponseMixin, LoginRequiredMixin, CreateView):
    model = Composition
    template_name = 'exquisitecorpse/composition_create.html'
    form_class = CompositionForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CompositionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('corpse:composition_details', args=(self.object.pk,))


class CompositionUpdate(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Composition
    fields = ['max_users', 'title', 'turns', 'min_part_chars', 'max_part_chars', 'join_policy', 'public_result']
    #template_name = 'exquisitecorpse/composition_update.html'


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
