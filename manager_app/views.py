import os
import threading
from email.mime.image import MIMEImage

import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib.auth import login, logout
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.utils import timezone

from .forms import *

# Create your views here.

def home(request):
    return render(request, 'manager_app/home.html')

def calculate_balance(request):
    total_income = sum(income.value for income in Income.objects.filter(user = request.user))
    total_savings = sum(savings.value for savings in Savings.objects.filter(user = request.user))
    total_expenditure = sum(expenditure.value for expenditure in Expenditure.objects.filter(user = request.user))
    balance = total_income-total_expenditure-total_savings
    if(total_savings < 0.3*balance): #mail them about low savings
        msg = """
            Hi %s,
            Your account savings are Rs %.2f, which is less than 30%% of the balance amount(Rs. %.2f). 
            Kindly take necessary steps.
            """ % (request.user, total_savings, balance,)
        email = EmailMultiAlternatives(
            'Your expense manager app: Account is low on savings',
            msg,
            "djscecomputers@gmail.com",
            [request.user.email],
            reply_to=['bhatianilay@gmail.com'],
        )
        htmly = get_template('manager_app/low_savings.html')
        html_content = htmly.render({'username' : request.user, 'savings' : total_savings, 'balance' : balance})
        email.attach_alternative(html_content, "text/html")
        email.mixed_subtype = 'related'

        p = 'static/manager_app/'
        for f in ['logo.png', 'savings.png']:
            fp = open(os.path.join(os.path.dirname(__file__), p+f), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(f))
            email.attach(msg_img)
        email.attach_file('manager_app/static/manager_app/savings.png')
        email.send()
    return balance

def generate_plot(request, something):
    sizes = []
    colors_set = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'blue']
    if(something == 'income'):
        labels = [choice[0] for choice in Income.SOURCE_CHOICES]
        for label in labels:
            sizes.append(sum(income.value for income in Income.objects.filter(user = request.user, source = label)))
    elif(something == 'savings'):
        labels = [choice[0] for choice in Savings.CATEGORY_CHOICES]
        for label in labels:
            sizes.append(sum(savings.value for savings in Savings.objects.filter(user = request.user, category = label)))
    elif(something == 'expenditure'):
        labels = [choice[0] for choice in Expenditure.CATEGORY_CHOICES]
        for label in labels:
            sizes.append(sum(expenditure.value for expenditure in Expenditure.objects.filter(user = request.user, category = label)))
    colors = colors_set[0:len(sizes)]

    #Plot
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig('manager_app/static/manager_app/' + something + '.png')
    plt.show()
        




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
            'org' : OrganisationForm(request.POST),
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

#view for viewing income, savings, etc
def view_something(request, something):
    options = {
        'income' : Income.objects.filter(user = request.user).order_by('-date_received'),
        'savings' : Savings.objects.filter(user = request.user).order_by('-date_saved'),
        'expenditure' : Expenditure.objects.filter(user = request.user).order_by('-date_spent'),
        'org' : Organisation.objects.all()
    }
    that_things = options[something] #eg. incomes = Income.objects.all()...
    #generate_plot(request, something)
    t = threading.Thread(target=generate_plot, args=[request, something])
    # We want the program to wait on this thread before shutting down.
    t.setDaemon(False)
    t.start()
    total = 0
    if(something != 'org'):
        for that_thing in that_things:
            total += that_thing.value
    return render(request, 'manager_app/view_' + something + '.html', {'that_things' : that_things, 'total' : total})

#for clearing this month's figures and fresh start for new month
def clear_figures(request):
    total_income = sum(income.value for income in Income.objects.filter(user = request.user))
    total_savings = sum(savings.value for savings in Savings.objects.filter(user = request.user))
    total_expenditure = sum(expenditure.value for expenditure in Expenditure.objects.filter(user = request.user))
    balance = total_income-total_expenditure-total_savings
    msg = """
            Hi %s,
            Your account summary
            Income : %.2f
            Savings : %.2f
            Expendture : %.2f
            Balance : %.2f
            Sincerely,
            Your expense manager app
            """ % (request.user, total_income, total_savings, total_expenditure, balance)
    email = EmailMultiAlternatives(
        'Your expense manager app: The month in review',
        msg,
        "djscecomputers@gmail.com",
        [request.user.email],
        reply_to=['bhatianilay@gmail.com'],
    )
    htmly = get_template('manager_app/monthly_report.html')
    html_content = htmly.render({'username' : request.user, 'income' : total_income, 'savings' : total_savings, 'expenditure' : total_expenditure})
    email.attach_alternative(html_content, 'text/html')
    email.mixed_subtype = 'related'

    p = 'static/manager_app/'
    for f in ['logo.png', 'income.png', 'savings.png', 'expenditure.png']:
        fp = open(os.path.join(os.path.dirname(__file__), p+f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        email.attach(msg_img)

    email.attach_file('manager_app/static/manager_app/income.png')
    email.attach_file('manager_app/static/manager_app/savings.png')
    email.attach_file('manager_app/static/manager_app/expenditure.png')
    email.send()
    Income.objects.filter(user = request.user).delete()
    Savings.objects.filter(user = request.user).delete()
    Expenditure.objects.filter(user = request.user).delete()
    return redirect('profile')

