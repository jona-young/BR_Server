import datetime
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


class CIMemberListView(LoginRequiredMixin, ListView):
    model = courtInf
    template_name = 'courtinfractions/member_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    #pulls all records of those by specific name
    def get_queryset(self):
        return courtInf.objects.filter(name_id=self.kwargs.get('name_id')).order_by('-date_created')


class CIDateListView(LoginRequiredMixin, ListView):
    model = courtInf
    template_name = 'courtinfractions/date_records.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'records'
    paginate_by = 5

    #pulls all records of those by a specific date
    def get_queryset(self):
        return courtInf.objects.filter(date=self.kwargs.get('date')).order_by('-courtTime')


class CIDetailView(LoginRequiredMixin, DetailView):
    model = courtInf


class CIListView(LoginRequiredMixin, ListView):
    model = courtInf
    template_name = 'courtinfractions/summary.html'
    context_object_name = 'records'
    ordering = '-date_created'
    paginate_by=12

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
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
                return courtInf.objects.order_by('-date_created').all()
            else:
                return courtInf.objects.filter(date__month=month,
                                               date__year=year).order_by('-date_created').all()


class CICreateView(LoginRequiredMixin, CreateView):
    model = courtInf
    fields = ['sport', 'name', 'infraction', 'date', 'courtTime', 'notes']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        if 'single' in self.request.POST:
            return redirect('CI-summary')
        else:
            return redirect('CI-new')


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
def CIEmailFormView(request):
    context = {}

    if request.method == 'POST':
        forms = multipleForm(request.POST)
        if forms.is_valid():
            #pulls selected records/objects to carry on with email automation
            checkList = request.POST.getlist('Choices')
            #calls a function script to email selected choices
            emailAutomation(checkList)
        return redirect('CI-summary')

    #If the date is Monday all court infraction objects pulled from the past week
    if datetime.date.today().weekday() == 0:
        beg_date = (datetime.date.today() + datetime.timedelta(days=-7)).strftime('%b %d')
        end_date = datetime.datetime.today().strftime('%b %d')

    #If the date is not Monday, all court infractions still pulled from past week starting Monday
    else:
        day_mod = datetime.date.today().weekday()

        beg_date = (datetime.datetime.today() + datetime.timedelta(days=-(7+day_mod))).strftime('%b %d')
        end_date = (datetime.datetime.today() + datetime.timedelta(days=-day_mod)).strftime('%b %d')

    context = {
        'selectForm': multipleForm(),
        'beg_date': beg_date,
        'end_date': end_date,
    }

    return render(request, 'courtinfractions/courtInf_emailselect.html', context)

@login_required
def CITableView(request):
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
    context = {}
    dict = {}

    if request.method == 'GET':
        print('A name filter has been entered')
        letter = request.GET.get('alphabet')
        #alphabet_letter = request.GET.get('alphabet')
        #letter = alphabet_list[alphabet_letter]
        if letter is None:
            print('no letter: ', str(letter))
            infractions = courtInf.objects.order_by('-date').all()
            print('Letter is none: ', infractions)
        else:
            print('some letter: ', str(letter))
            infractions = courtInf.objects.filter(name__memberName__startswith=letter).order_by('name').all()
            print('Letter is something', infractions)

    #counts number of infractions per member name
    for inf in infractions:
        if inf.name in dict:
            dict[inf.name] += 1
        else:
            dict[inf.name] = 1
    sortedDict = OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))

    context['table']=sortedDict.items()
    context = {
        'table': sortedDict.items(),
        'alphabet_list': alphabet_list
    }
    return render(request, 'courtinfractions/courtInf_table.html', context)

#Multi-Form Create page
@login_required
def CIFormsetView(request):
    context = {}

    CIFormset = modelformset_factory(
        courtInf, fields = ['sport', 'name', 'infraction',
                            'date', 'courtTime', 'notes'], extra=4)
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
