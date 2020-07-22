from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    #If the form has been filled out, then it will attempt to create a new account
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #if the information in the form is valid of a new account, it will save
        #create, and redirect back to the main page
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are not able to login!')
            return redirect('login')
    #if the form has not been filled out, it will open the form as a new page
    else:
        form = UserRegisterForm()
    #if the form has been filled out but it is not valid, it will redirect to (below)
    return render(request, 'users/register.html', {'form':form})

#A decorator provides functionality to an existing function
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
