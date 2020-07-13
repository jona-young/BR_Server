from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import memberRecord
from .forms import createForm
from django.contrib.auth.decorators import login_required

class MEListView(ListView):
    model = memberRecord
    template_name = 'memberexperience/memberRecord_summary.html'
    context_object_name = 'objects'
    ordering = '-id'
    paginate_by = 10

class MEDetailView(DetailView):
    model = memberRecord

class MEUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = memberRecord
    form_class = createForm
    template_name = 'memberexperience/memberRecord_update.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        updateForm = form.save(commit=False)
        updateForm.save()
        updateForm.sportPrefs.set(form.cleaned_data.get('sportPreference'))
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

#TODO - Remember to call ModelMultipleChoiceField to allow the user to select multiple options
@login_required
def MECreateView(request):
    context = {}

    create = createForm()


    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            sendForm = form.save(commit=False)
            sendForm.author = request.user
            sendForm.save()
            sendForm.sportPrefs.set(form.cleaned_data.get('sportPreference'))
            form.save_m2m()

            return redirect('ME-summary')

    context['create']=create
    return render(request, 'memberexperience/memberRecord_form.html', context)
