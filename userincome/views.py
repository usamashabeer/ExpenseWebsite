import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    src = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    currency = UserPreference.objects.get(user=request.user.id).currency

    currency = currency.split('-')[0]
    context = {
        'page_obj': page_obj,
        'income': income,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    src = Source.objects.all()
    context = {
        'sources': src,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        desc = request.POST['description']
        date = request.POST['income_date']
        src = request.POST['source']

        if not amount and desc and date and src:
            messages.error(request, 'Please fill all the required field')
            return render(request, 'income/add_income.html', context)
        UserIncome.objects.create(owner=request.user, amount=amount, description=desc, date=date, source=src)
        messages.success(request, 'Income record saved successfully')
        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    user_income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': user_income,
        'values': user_income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        desc = request.POST['description']
        date = request.POST['income_date']
        src = request.POST['source']

        if not amount and desc and date and src:
            messages.error(request, 'Please fill all the required field')
            return render(request, 'income/edit_income.html', context)
        user_income.owner = request.user
        user_income.amount = amount
        user_income.description = desc
        user_income.date = date
        user_income.source = src
        user_income.save()
        messages.success(request, 'Income record updated successfully')
        return redirect('income')


def delete_income(request, id):
    user_income = UserIncome.objects.get(pk=id)
    user_income.delete()
    messages.success(request, 'Income deleted')
    return redirect('income')

def search_income(request):
    print('hello i am in there')
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        # print(expenses)

        data = income.values()
        return JsonResponse(list(data), safe=False)

# def search_income(request):
#     return render(request,'income/index.html')
