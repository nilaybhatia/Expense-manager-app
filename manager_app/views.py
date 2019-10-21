from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import SignUpForm
from django.contrib.auth import login, logout
# Create your views here.

def home(request):
    return render(request, 'manager_app/home.html')
def profile(request):
    return render(request, 'manager_app/profile.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'manager_app/signup.html', {'form': form})
