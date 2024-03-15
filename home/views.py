from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from home.models import *
from blog.models import *
from home.forms import *
from django.contrib.auth import authenticate,login,get_user_model


user_model=get_user_model()

# Create your views here.

def index(request):
    return render(request, 'index.html')



def SignUp(request):
    if request.method == 'POST':
        is_doc=request.POST.get('check')
        if is_doc:
            doc_id=request.POST.get('doc_id')
        user_form=UserCreateForm(request.POST)
        profile=profile_form(request.POST,request.FILES)
        if user_form.is_valid() and profile.is_valid():
            user=user_form.save()
            pro=profile.save(commit=False)
            pro.user=user
            pro.is_doctor=bool(is_doc)
            if is_doc:
                pro.doc_id=doc_id
            pro.save()
            return redirect(reverse_lazy("home:home"))
    return render(request, 'signup.html',{'Userform':UserCreateForm,'profile_form':profile_form,})

@login_required
def dashboard(request):
    user=request.user
    profile_data=profile.objects.filter(user=user.id).all()
    return render(request, 'dashboard.html',{'user':user, 'profile':profile_data[0]})

def login_user(request,pk):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if pk=='1':
            doc_id=request.POST.get('doc_id')
        user=authenticate(username=username, password=password)
        if user is not None:
            user_info=profile.objects.filter(user=user.id).all()
            if pk=='1':
                if user_info[0].doc_id==int(doc_id):
                    login(request,user)
                    return redirect(reverse_lazy('home:dashboard'))
            elif pk=='0':
                login(request,user)
                return redirect(reverse_lazy('home:dashboard'))
            else:
                return render(request,'login.html',{'error': "Invalid Doctor ID"})
        else:
            return render(request,'login.html',{"error": "Invalid Credentials"})
    return render(request, 'login.html',{"pk_user":pk})

def contact(request):
    if request.method == 'POST':
        cont=contact_form(request.POST)
        cont.save()
        return redirect(reverse_lazy('home:home'))
    return render(request,'contact.html',{'form':contact_form})

@login_required
def user_profile(request):
    user=request.user
    all_posts=post.objects.filter(user=user)
    pro=profile.objects.filter(user=user)[0]
    if request.user.profile.is_doctor:
        app=appointment_model.objects.filter(doctor_email=request.user.email).order_by("start_date")
    else:
        app=appointment_model.objects.filter(user=user).all().order_by('start_date')
    return render(request, 'profile.html', {
        'published': all_posts.filter(published=True).all().order_by("-id"),
        'not_published': all_posts.filter(published=False).all().order_by("-id"),
        'profile':pro,
        'appointments':app
                                            })

class PasswordChangeView(PasswordChangeView,LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name='pasword_change.html'
    success_url=reverse_lazy("home:profile")

class update_profile_data(UpdateView):
    model=profile
    form_class=profile_form
    template_name="update_profile.html"
    success_url=reverse_lazy("home:profile")

    def form_valid(self, form):
        form2=form.save(commit=False)
        if not form2.is_doctor:
            form2.doc_id=None
        form2.save()
        return super().form_valid(form)
    



class book_appointment(ListView):
    model=profile
    template_name='doctors_list.html'
    def get_queryset(self):
        QuerySet=profile.objects.filter(is_doctor=True).all()
        return QuerySet
    
def appointment(request,pk):
    user_data=profile.objects.filter(id=pk).all()
    if request.method == "POST":
        user=get_object_or_404(user_model,pk=request.user.id)
        doctor_name=request.POST.get('doctor_name')
        doctor_email=request.POST.get('doctor_email')
        speciality=request.POST.get('speciality')
        start_date=request.POST.get('start_date')
        start_time=request.POST.get('start_time')
        ins=appointment_model.objects.create(user=user, start_date=start_date, start_time=start_time,speciality=speciality,doctor_name=doctor_name,doctor_email=doctor_email)
        ins.save()
        return redirect(reverse_lazy('home:confirmation',kwargs={'pk': ins.id}))
    return render(request,'appointment.html',{'user_data':user_data[0]})


# ////--------------- Calendar Configuration -----------------////

import datetime
from datetime import timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


scopes = ['https://www.googleapis.com/auth/calendar']
# calender_id='3e3559b0748d47a350bfa691fab857a6536e0dc163a2cabcb14a05755897786e@group.calendar.google.com' custom calendar
calender_id='primary' # general main calendar


def calender_setup():
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service
    
# ////--------------- Calendar Configuration Completed -----------------////


def confirmation(request,pk):
    appoint=appointment_model.objects.get(id=pk)
    appoint.confirm_appointment()
    start = str(appoint.start_date) +' '+ str(appoint.start_time)
    start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
    end_time  = start_time + timedelta(minutes=45)
    timezone = 'Asia/Kolkata'

    service=calender_setup()
    event={
        "summary": 'Doctor Apointment',
        "location":"Online Meeting",
        'description':"For appoitment reagrding Speciality in "+appoint.speciality,
        'start':{
            'dateTime': start_time.isoformat(),
            'timeZone': timezone,
        },
        'end':{
            'dateTime': end_time.isoformat(),
            'timeZone': timezone,
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': appoint.user.email},
            {'email': appoint.doctor_email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 3 * 60},
            {'method': 'popup', 'minutes': 15},
            ]
        },
    }
    event = service.events().insert(calendarId=calender_id, body=event).execute()
    appoint.enter_event_id(event['id'])
    appoint.enter_end_time(end_time.time().replace(microsecond=0))
    return redirect(reverse_lazy('home:appointment_details', kwargs={'pk': pk}))    

class appointment_details(DetailView):
    model=appointment_model
    template_name='appointment_details.html'


def dele_confirm(request,pk):
    return render(request, 'confirm.html',{'appointment':appointment_model.objects.filter(id=pk).all()[0],})

def delete_appointment(request,pk):
    appoint_delete=appointment_model.objects.filter(id=pk).all()[0]
    service=calender_setup()
    service.events().delete(calendarId=calender_id, eventId=appoint_delete.event_id).execute()
    appoint_delete.delete()
    return redirect(reverse_lazy("home:profile"))