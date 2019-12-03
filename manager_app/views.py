from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import *
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

#something can be income, savings, or expenditure
#view for adding an income, savings or expenditure
def something_new(request, something):
    options = {
            'income' : IncomeForm(request.POST),
            'savings' : SavingsForm(request.POST),
            'expenditure' : ExpenditureForm(request.POST),
    }
    if request.method == "POST":
        form = options[something]
        if form.is_valid():
            that_thing = form.save(commit=False) #eg. income = form.save()
            that_thing.user = request.user
            that_thing.save()
            return redirect('view_something', something = something)
    else:
        form = options[something]
        return render(request, 'manager_app/something_edit.html', {'form': form, 'something': something})

def view_something(request, something):
    options = {
        'income' : Income.objects.all().order_by('-date_received'),
        'savings' : Savings.objects.all().order_by('-date_saved'),
        'expenditure' : Expenditure.objects.all().order_by('-date_spent'),
    }
    that_things = options[something] #eg. incomes = Income.objects.all()...
    return render(request, 'manager_app/view_' + something + '.html', {'that_things' : that_things})