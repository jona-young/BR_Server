from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
import datetime
from .models import memberRecord
from .forms import createForm

class MEListView(LoginRequiredMixin, ListView):
    model = memberRecord
    template_name = 'memberexperience/memberRecord_summary.html'
    context_object_name = 'objects'
    paginate_by = 10

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    year_list = list(range(memberRecord.objects.earliest('joinDate').joinDate.year,
                           (memberRecord.objects.latest('joinDate').joinDate.year)+1))

    #passing month and year options to date search filter
    def get_context_data(self, **kwargs):
        context = super(MEListView, self).get_context_data(**kwargs)
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
                return memberRecord.objects.order_by('-joinDate').all().order_by('-id')
            else:
                return memberRecord.objects.filter(joinDate__month=month,
                                                   joinDate__year=year).order_by('-id').all()

class MEDetailView(LoginRequiredMixin, DetailView):
    model = memberRecord

class MEUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = memberRecord
    form_class = createForm
    template_name = 'memberexperience/memberRecord_update.html'

    #updates the form including many-to-many sportPrefs with save_m2m()
    def form_valid(self, form):
        form.instance.author = self.request.user
        updateForm = form.save(commit=False)
        updateForm.save()
        updateForm.sportPrefs.set(form.cleaned_data.get('sportPrefs'))
        form.save_m2m()

        return redirect('ME-summary')

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.author:
            return True
        return False

class MEDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = memberRecord
    success_url = '/memberexperience/summary/'

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.author:
            return True
        return False

@login_required
def MECreateView(request):
    context = {}
    create = createForm()

    # updates the form including many-to-many sportPrefs with save_m2m()
    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            sendForm = form.save(commit=False)
            sendForm.author = request.user
            sendForm.save()
            sendForm.sportPrefs.set(form.cleaned_data.get('sportPrefs'))
            form.save_m2m()

            return redirect('ME-summary')

    context['create']=create
    return render(request, 'memberexperience/memberRecord_form.html', context)
