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
from .models import courtInf
from .forms import multipleForm
from .scripts import emailAutomation
from collections import OrderedDict


class CIMemberListView(ListView):
    model = courtInf
    template_name = 'courtinfractions/member_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    #pulls all records of those by specific name
    def get_queryset(self):
        return courtInf.objects.filter(name_id=self.kwargs.get('name_id')).order_by('-date_created')

class CIDateListView(ListView):
    model = courtInf
    template_name = 'courtinfractions/date_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    #pulls all records of those by a specific date
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

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    year_list = list(range(courtInf.objects.earliest('date').date.year,
                           (courtInf.objects.latest('date').date.year)+1))

    #passing month and year options to date search filter
    def get_context_data(self, **kwargs):
        context = super(CIListView, self).get_context_data(**kwargs)
        context.update({
            'month_list': self.month_list,
            'year_list': self.year_list
        })
        return context

    #pulls selected month and year and queries objects in model of that month and year
    def get_queryset(self):
        if self.request.method == 'GET':
            print('A date query has been entered')
            month = self.request.GET.get('month')
            year = self.request.GET.get('year')
            print('month: ', str(month))
            print('year: ', str(year))
            if month is None or year is None:
                return courtInf.objects.order_by('-date').all()
            else:
                return courtInf.objects.filter(date__month=month,
                                                   date__year=year).order_by('-date').all()

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

#Multi-Form Create page
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

'''
#Email Automation page
class CIEmailFormView(LoginRequiredMixin, ListView):
    model = courtInf
    form_class = multipleForm
    template_name = 'courtinfractions/courtInf_emailselect.html'
    context_object_name = 'records'
    ordering = '-date_created'

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    year_list = list(range(courtInf.objects.earliest('date').date.year,
                           (courtInf.objects.latest('date').date.year)+1))

    #passing month and year options to date search filter
    def get_context_data(self, **kwargs):
        context = super(CIEmailFormView, self).get_context_data(**kwargs)
        context.update({
            'month_list': self.month_list,
            'year_list': self.year_list
        })
        return context

    #pulls selected month and year and queries objects in model of that month and year
    def get_queryset(self):
        if self.request.method == 'GET':
            print('A date query has been entered')
            month = self.request.GET.get('month')
            year = self.request.GET.get('year')
            print('month: ', str(month))
            print('year: ', str(year))
            
            if month is None or year is None:
                return courtInf.objects.order_by('-date').all()
            else:
                return courtInf.objects.filter(date__month=month,
                                                   date__year=year).order_by('-date').all()

    def form_valid(self):
        checkList = self.request.POST.getlist('Choices')
        # calls a function script to email selected choices
        emailAutomation(checkList)
        return redirect('CI-summary')

'''

@login_required
def CIEmailFormView(request):
    context = {}

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    year_list = list(range(courtInf.objects.earliest('date').date.year,
                           (courtInf.objects.latest('date').date.year)+1))

    if request.method == 'POST':
        forms = multipleForm(request.POST)
        if forms.is_valid():
            #pulls selected records/objects to carry on with email automation
            checkList = request.POST.getlist('Choices')
            #calls a function script to email selected choices
            emailAutomation(checkList)
        return redirect('CI-summary')

    #pulls selected month and year and queries objects in model of that month and year
    if request.method == 'GET':
        print('A date query has been entered')
        month = request.GET.get('month')
        year = request.GET.get('year')
        print('month: ', str(month))
        print('year: ', str(year))
        #TODO: Figure out how to pass filtered objects to multipleForm() because that is the form and where the data is pulled from
        if month is None or year is None:
            print('Month or Year is None')
        else:
            filter_obj = courtInf.objects.filter(date__month=month,
                                           date__year=year).order_by('-date').all()
            print(filter_obj)
            return request_context.push({'selectForm': filter_obj})


    context = {
        'selectForm': multipleForm(),
        'month_list': month_list,
        'year_list': year_list
    }

    return render(request, 'courtinfractions/courtInf_emailselect.html', context)

@login_required
def CITableView(request):
    context = {}
    dict = {}

    #counts number of infractions per member name
    infractions = courtInf.objects.all().order_by('name')
    for inf in infractions:
        if inf.name in dict:
            dict[inf.name] += 1
        else:
            dict[inf.name] = 1
    sortedDict = OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
    context['table']=sortedDict.items()
    return render(request, 'courtinfractions/courtInf_table.html', context)

