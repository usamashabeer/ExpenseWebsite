from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from userpreferences.models import UserPreference


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    cat = Category.objects.all()
    exp = Expense.objects.filter(owner=request.user)
    paginator = Paginator(exp, 3)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    currency = UserPreference.objects.get(user=request.user.id).currency

    currency = currency.split('-')[0]
    context = {
        'page_obj': page_obj,
        'expenses': exp,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


def app_expense(request):
    cat = Category.objects.all()
    context = {
        'categories': cat,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        desc = request.POST['description']
        date = request.POST['expense_date']
        cat = request.POST['category']

        if not amount and desc and date and cat:
            messages.error(request, 'Please fill all the required field')
            return render(request, 'expenses/add_expense.html', context)
        Expense.objects.create(owner=request.user, amount=amount, description=desc, date=date, category=cat)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    exp = Expense.objects.get(pk=id)
    cat = Category.objects.all()
    context = {
        'expense': exp,
        'values': exp,
        'categories': cat
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        print(request.POST)
        amount = request.POST['amount']
        desc = request.POST['description']
        date = request.POST['expense_date']
        cat = request.POST['category']

        if not amount and desc and date and cat:
            messages.error(request, 'Please fill all the required field')
            return render(request, 'expenses/edit_expense.html', context)
        exp.owner = request.user
        exp.amount = amount
        exp.description = desc
        exp.date = date
        exp.category = cat
        exp.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')


def delete_expense(request, id):
    exp = Expense.objects.get(pk=id)
    exp.delete()
    messages.success(request, 'Expense deleted')
    return redirect('expenses')


def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        print(expenses)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)
