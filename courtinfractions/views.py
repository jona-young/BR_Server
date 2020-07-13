from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import courtInf, contactInfo
from .forms import multipleForm
from .scripts import emailAutomation
from collections import OrderedDict


class CIMemberListView(ListView):
    model = courtInf
    template_name = 'courtinfractions/member_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    def get_queryset(self):
        return courtInf.objects.filter(name_id=self.kwargs.get('name_id')).order_by('-date_created')

class CIDateListView(ListView):
    model = courtInf
    template_name = 'courtinfractions/date_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    def get_queryset(self):
        return courtInf.objects.filter(date=self.kwargs.get('date')).order_by('-courtTime')


class CIDetailView(DetailView):
    model = courtInf

class CIListView(ListView):
    model = courtInf
    template_name = 'courtinfractions/summary.html'
    context_object_name = 'records'
    ordering = '-date_created'
    paginate_by=12

class CICreateView(LoginRequiredMixin, CreateView):
    model = courtInf
    fields = ['sport', 'name', 'infraction', 'date', 'courtTime', 'notes']

    def form_valid(self, form):
        form.instance.author = self.request.user

class CIUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = courtInf
    fields = ['sport', 'name', 'infraction', 'date', 'courtTime', 'notes']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.author:
            return True
        return False

class CIDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = courtInf
    success_url = '/courtinfractions/summary/'

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.author:
            return True
        return False

@login_required
def CIFormsetView(request):
    context = {}

    CIFormset = modelformset_factory(
        courtInf, fields = ['sport', 'name', 'infraction', 'date', 'courtTime', 'notes'], extra=4)
    formset = CIFormset(request.POST or None, queryset=courtInf.objects.none())

    if formset.is_valid():
        for form in formset:
            print(form.cleaned_data)
            if form['name'].value():
                form = form.save(commit=False)
                form.author = request.user
                form.save()
        return redirect('CI-summary')

    context['formset']=formset
    return render(request, 'courtinfractions/courtInf_multiform.html', context)

@login_required
def CIEmailFormView(request):
    context = {}

    selectForm = multipleForm()

    #Figure out how to bypass spam filters...sending to my Apple email account was blocked..
    if request.method == 'POST':
        forms = multipleForm(request.POST)
        if forms.is_valid():
            #Returns a list of the id's of the selected checkboxes...query the ids to pull info to email
            #obj = Class.objects.get(pk=this_object_id)
            checkList = request.POST.getlist('Choices')
            #Call a function script that handles querying the data and sendingt he email
            emailAutomation(checkList)
        return redirect('CI-summary')

    context['selectForm']=selectForm
    return render(request, 'courtinfractions/courtInf_emailselect.html', context)

@login_required
def CITableView(request):
    context = {}
    dict = {}

    '''
    IN FUTURE - If adding new columns based off date ranges, add filtered datasets and create
                new dictionaries to pass through to render...
    
    '''
    infractions = courtInf.objects.all().order_by('name')
    for inf in infractions:
        if inf.name in dict:
            dict[inf.name] += 1
        else:
            dict[inf.name] = 1
    sortedDict = OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
    context['table']=sortedDict.items()
    return render(request, 'courtinfractions/courtInf_table.html', context)

