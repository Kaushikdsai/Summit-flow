from datetime import datetime, timedelta, timezone
import json
import math
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User, PasswordReset, UserAchievements, UserData, UserMetrics
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .forms import RegistrationForm, LoginForm, TimerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from datetime import date
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

restricted_websites=[]

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
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

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

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
            UserMetrics.objects.create(user=user,rank=0,rating=0,total_hours=0)
            UserAchievements.objects.create(user=user,bronze_badges=0,silver_badges=0,gold_badges=0)
            calculateRank()
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
    websites=request.GET.get('websites','')
    if not break_duration:
        break_duration=None
    if not websites:
        websites=None
    context = {
        'focus_duration':focus_duration,
        'break_duration':break_duration,
        'websites':websites
    }
    return render(request,'session.html',context)

@csrf_exempt
def restricted_urls(request):
    print("RU")
    if(request.method=="GET"):
        print("GET")
        return JsonResponse({"restricted_urls":restricted_websites})
    
    elif(request.method=="POST"):
        print("POST")
        data=json.loads(request.body)
        if "restricted_urls" in data:
            urls=data.get("restricted_urls",[])
            urls=list(set(urls))
            return JsonResponse({"status":"success", "restricted_urls":restricted_websites})
        else:
            return JsonResponse({"status":"error","message":"Invalid data"})
        
    else:
        return JsonResponse({"message":"Invalid Request Method!"})

def sessionDetails(request):
    user=request.user

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
        hours=session_seconds/3600
        metrics.total_hours+=hours
        metrics.rating+=session_seconds
        metrics.save()
        calculateRank()
        
        today=date.today()
        user_data,created=UserData.objects.get_or_create(user=request.user,date=today,defaults={'hours':0})
        user_data.hours+=hours
        user_data.save()
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
        achievements, created=UserAchievements.objects.get_or_create(user=metrics.user)
        bronze=math.floor(metrics.rating/30)
        silver=math.floor(metrics.rating/50)
        gold=math.floor(metrics.rating/100)
        achievements.bronze_badges=bronze
        achievements.silver_badges=silver
        achievements.gold_badges=gold
        achievements.save()
        context = { 
            'name': user.name,
            'user_id': metrics.user.id,
            'rank': metrics.rank,
            'rating': metrics.rating,
            'total_hours': metrics.total_hours,  
            'bronze':bronze,
            'silver':silver,
            'gold':gold
        }
    except UserMetrics.DoesNotExist:
        context = {
            'error': 'Metrics not found for this user.'
        }
    return render(request,'user_dashboard.html',context)

def bike(request):
    return render(request,'bike1.html')

def dashboard(request):
    return render(request,'user_dashboard.html')

def leaderboard(request):
    all_user_metrics=UserMetrics.objects.select_related('user').all().order_by('-rating')
    leaderboard_data=[]
    for metrics in all_user_metrics:
        try:
            achievements=UserAchievements.objects.get(user=metrics.user)
        except UserAchievements.DoesNotExist:
            achievements=UserAchievements(user=metrics.user)
            bronze=math.floor(metrics.rating/30)
            silver=math.floor(metrics.rating/50)
            gold=math.floor(metrics.rating/100)
            achievements.bronze_badges=bronze
            achievements.silver_badges=silver
            achievements.gold_badges=gold
            achievements.save()
        leaderboard_data.append({
                'name': metrics.user.name,
                'user_id': metrics.user.id,
                'rank': metrics.rank,
                'rating': metrics.rating,
                'total_hours': metrics.total_hours,  
                'bronze':achievements.bronze_badges,
                'silver':achievements.silver_badges,
                'gold':achievements.gold_badges
        })
    context = {
        'leaderboard_data':leaderboard_data
    }
    return render(request,'leaderboard.html',context)

def fetch_chart_data(request):
    range_type=request.GET.get('range','days')
    today=date.today()
    data=[]
    if range_type=="days":
        start_date=today.replace(day=1)
        if(today.month!=12):
            end_date=today.replace(month=today.month+1,day=1)-timedelta(days=1)
        else:
            end_date=today.replace(month=today.month,day=31)

        days=[]
        num_of_days=(end_date-start_date).days+1
        for i in range(num_of_days):
            curr_date=start_date+timedelta(days=i)
            date_str=curr_date.strftime("%Y-%m-%d")
            days.append(date_str)
        user_data=UserData.objects.filter(user=request.user,date__month=today.month,date__year=today.year).values('date').annotate(hours=Sum('hours'))

        data_dict={}
        for val in user_data:
            key=val['date'].strftime("%Y-%m-%d")
            value=val['hours']
            data_dict[key]=value

        for day in days:
            data.append({
                'label':day,
                'value':data_dict.get(day,0)
            })

    elif range_type=="months":
        curr_year=today.year
        months=[]
        for month in range(1,13):
            month_name=datetime(curr_year,month,1).strftime("%B")
            months.append(month_name)
        user_data=UserData.objects.filter(user=request.user, date__year=curr_year)
        user_data=user_data.annotate(month=ExtractMonth('date'))
        grouped_data=user_data.values('month').annotate(hours=Sum('hours'))
        data_dict={}
        for val in grouped_data:
            key=val['month']
            value=val['hours']
            data_dict[key]=value
        for i in range(12):
            month_name=months[i]
            month_num=i+1
            total_hours=data_dict.get(month_num,0)
            data.append({'label':month_name,
                         'value':total_hours})
            
    elif range_type=="years":
        curr_year=today.year
        start_year=int(curr_year)-10
        user_data=UserData.objects.filter(user=request.user)
        user_data=user_data.annotate(year=ExtractYear('date'))
        grouped_data=user_data.values('year').annotate(hours=Sum('hours'))

        data_dict={}
        for val in grouped_data:
            key=val['year']
            value=val['hours']
            data_dict[key]=value

        for year in range(start_year,curr_year+1):
            data.append({
                'label':year,
                'value':data_dict.get(year,0)
            })

    return JsonResponse({'data':data})
