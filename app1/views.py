from datetime import timezone
import json
import math
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User, PasswordReset, UserMetrics
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .forms import RegistrationForm, LoginForm, TimerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                print(f"User found: {user.email}")
                if user.check_password(password):
                    request.session['user_id']=user.id
                    print(f"Session user_id after login: {request.session.get('user_id')}")
                    messages.success(request, "Logged in!")
                    return redirect('timer')
                else:
                    messages.error(request, "Email or password is not correct!")
            except User.DoesNotExist:
                messages.error(request,"Email or password is not correct!")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            print("Before saving the user")
            user.save()
            print("User saved successfully!")
            return redirect('login')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field.capitalize()}: {error}")
    else:
        form=RegistrationForm()
    return render(request,'register.html',{'form':form})

def timer(request):
    if request.method=='POST':
        form=TimerForm(request.POST)
        if form.is_valid():
            focus_duration=form.cleaned_data['focus_duration']
            break_duration=form.cleaned_data['break_duration']
            if not break_duration:
                break_duration=''
            websites=form.cleaned_data.get('websites','')
            
            query_params = urlencode({
                'focus_duration': focus_duration,
                'break_duration': break_duration,
                'websites': websites,
            })
            url=reverse('session')+"?"+query_params
            return redirect(url)
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form=TimerForm()
    return render(request,'timer.html', {'form':form})

def session(request):
    focus_duration=request.GET.get('focus_duration')
    break_duration=request.GET.get('break_duration','')
    if not break_duration:
        break_duration=None
    websites=request.GET.get('websites')
    context = {
        'focus_duration':focus_duration,
        'break_duration':break_duration,
        'websites':websites
    }
    return render(request,'session.html',context)

def mailSent(request,reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request,'forgot_password/mail_sent.html')
    else:
        messages.error(request,"Invalid reset ID!")
        return redirect('forgot-password')

def resetDone(request):
    return render(request,'forgot_password/reset_complete.html')

def newPassword(request,reset_id):
    try:
        reset_entry=PasswordReset.objects.get(reset_id=reset_id)
        if request.method=="POST":
            password=request.POST.get('new_password1')
            confirm_password=request.POST.get('new_password2')
            passwords_have_error=False
            if password!=confirm_password:
                passwords_have_error=True
                messages.error(request,'Passwords do not match!')

            expiration_time=reset_id.created_when+timezone.timedelta(minutes=10)

            if timezone.now()>expiration_time:
                passwords_have_error=True
                messages.error(request,"Reset link has expired!")

            if not passwords_have_error:
                user=reset_id.user
                user.set_password(password)
                user.save()
                reset_id.delete()
                messages.success(request,'Password reset. Proceed to login!')
                return redirect('login')
            
            else:
                return redirect('new-password',reset_id=reset_id.reset_id)

    except PasswordReset.DoesNotExist:
        messages.error(request,'Invalid_reset_id')
        return redirect('forgot-password')
    
    return render(request,'forgot_password/new_password.html')

def forgotPassword(request):
    if request.method=="POST":
        email = request.POST.get('email')
        try:
            user=User.objects.get(email=email)
            new_password_reset=PasswordReset(user=user)
            new_password_reset.save()
            password_reset_url=reverse('new-password',kwargs={'reset_id':new_password_reset.reset_id})
            full_password_reset_url=f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body=f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send(fail_silently=True)

            messages.success(request, "Password reset request processed successfully! Check your email.")
            return redirect('mail-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, "No user found with that email!")
            return redirect('forgot-password')

    return render(request,"forgot_password/reset_password.html")

@login_required
def update_metrics(request):
    if request.method=="POST":
        data=json.loads(request.body)
        session_seconds=data.get('session_seconds',0)
        metrics, created=UserMetrics.objects.get_or_create(user=request.user)
        hours=math.floor(session_seconds/3600)
        metrics.total_hours+=hours
        metrics.rating+=session_seconds
        metrics.save()
        calculateRank()
        responseData={
            'total_hours':metrics.total_hours,
            'rating': metrics.rating,
            'rank':metrics.rank
        }
        return JsonResponse(responseData)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def calculateRank():
    all_metrics=UserMetrics.objects.all().order_by('-rating')
    rank=1
    for metrics in all_metrics:
        metrics.rank=rank
        metrics.save()
        rank+=1

@login_required
def user_dashboard(request):
    try:
        user=request.user
        metrics = UserMetrics.objects.get(user=user) 
        context = {
            'name': user.name,
            'user_id': user.id,
            'rank': metrics.rank,
            'rating': metrics.rating,
            'total_hours': metrics.total_hours,
        }
    except UserMetrics.DoesNotExist:
        context = {
            'error': 'Metrics not found for this user.'
        }
    return render(request,'user_dashboard.html',context)

def bike(request):
    return render(request,"bike1.html")

def dashboard(request):
    return render(request,"user_dashboard.html")