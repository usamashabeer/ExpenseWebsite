from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth


# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Not proper email format'}, status=400)
        return JsonResponse({'email_valid': True})


class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Only Contain Alphanumeric'}, status=400)
        # if User.objects.filter(username=username).exists():
        #     return JsonResponse({'username_error': 'User name exist already'}, status=500)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get user data
        # validate
        # create user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValue': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password Too Short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                # user.is_active = True
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'https://' + domain + link
                email_subject = 'Activation mail'
                email_body = 'Hi' + user.username + "Please use to link to verify your account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@example.com',
                    [email]
                )
                email.send(fail_silently=False)
                messages.success(request, 'User has been created Successfully')
                return render(request, 'authentication/register.html', context)
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            print(uidb64, '/', token)
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.checktoken(user, token):
                return redirect('login' + "?message=" + 'User already activated.')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, "Account activated Successfully")
            return redirect('login')
        except Exception as ex:
            print(ex)
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # print(username,password)

        if username and password:
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                auth.login(request, user)
                messages.success(request, 'Welcome ' + user.username + "! you are now logged in")
                return redirect('expenses')

            messages.error(request, 'Invalid credentials, try again')

            return render(request, 'authentication/login.html')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect('login')
