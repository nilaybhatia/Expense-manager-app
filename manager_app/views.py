from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
# Create your views here.

def home(request):
    return render(request, 'manager_app/home.html')

def calculate_balance(request):
    total_income = sum(income.value for income in Income.objects.filter(user = request.user))
    total_savings = sum(savings.value for savings in Savings.objects.filter(user = request.user))
    total_expenditure = sum(expenditure.value for expenditure in Expenditure.objects.filter(user = request.user))
    balance = total_income-total_expenditure-total_savings
    if(balance <= 1000000000):
        msg = """
            Hi %s,
            Your account savings are Rs %.2f, which is less than 30%% of the balance amount(Rs. %.2f). 
            Kindly take necessary steps.
            """ % (request.user, total_savings, balance,)
        send_mail(
            'Your expense manager app: Account is low on savings',
            msg,
            "example@gmail.com",
            [request.user.email],
            fail_silently=False,
        )
    return balance
def profile(request):
    return render(request, 'manager_app/profile.html', {'balance' : calculate_balance(request)})

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
        'income' : Income.objects.filter(user = request.user).order_by('-date_received'),
        'savings' : Savings.objects.filter(user = request.user).order_by('-date_saved'),
        'expenditure' : Expenditure.objects.filter(user = request.user).order_by('-date_spent'),
    }
    that_things = options[something] #eg. incomes = Income.objects.all()...
    total = 0
    for that_thing in that_things:
        total += that_thing.value
    total_income = sum(income.value for income in Income.objects.filter(user = request.user))
    return render(request, 'manager_app/view_' + something + '.html', {'that_things' : that_things, 'total' : total})