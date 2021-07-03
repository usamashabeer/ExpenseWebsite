from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.contrib import messages
from .models import UserPreference
import os, json


# Create your views here.
class UserPreferences(View):
    def load_currency(self):
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                a = {'name': k, 'value': v}
                currency_data.append(a)

        context = {'currencies': currency_data}
        return context

    def get(self, request):
        context = self.load_currency()
        return render(request, 'preferences/index.html', context)

    def post(self, request):
        currency = request.POST['currency']

        exists = UserPreference.objects.filter(user=request.user).exists()
        if exists:
            user_pref = UserPreference.objects.get(user=request.user)
            user_pref.currency = currency
            user_pref.save()
            messages.success(request, 'Changes saved')
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Changes saved')
        context = self.load_currency()

        return render(request, 'preferences/index.html', context)
