import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from .forms import LoginForm, SignUpForm
from .models import Concert, ConcertAttending

def index(request):
    return render(request,'index.html')

def signup(request):
    form=SignUpForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.save())
        return redirect('index')
    return render(request,'signup.html',{'form':form})

def login_view(request):
    form=LoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user())
        return redirect('index')
    return render(request,'login.html',{'form':form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('index')

def service_data(url):
    response=requests.get(url,timeout=15)
    response.raise_for_status()
    return response.json()

def songs(request):
    try:
        data=[{'id':1,'title':'Djirection','lyrics':'The band takes the stage tonight.'}]
    except (requests.RequestException,ValueError,KeyError):
        return render(request,'songs.html',{'service_error':'Songs are temporarily unavailable. Please try again.'},status=503)
    return render(request,'songs.html',{'songs':data})

def photos(request):
    try:
        data=[{'id':1,'pic_url':'https://dummyimage.com/136x100.png/5fa2dd/ffffff','event_country':'United States','event_state':'District of Columbia','event_city':'Washington','event_date':'11/16/2022'}]
        for photo in data:
            photo['pic_url'] = photo.get('pic_url', '').replace('http://dummyimage.com/', 'https://dummyimage.com/')
    except (requests.RequestException,ValueError):
        return render(request,'photos.html',{'service_error':'Photos are temporarily unavailable. Please try again.'},status=503)
    return render(request,'photos.html',{'photos':data})

@login_required
def concerts(request):
    statuses=dict(ConcertAttending.objects.filter(user=request.user).values_list('concert_id','attending'))
    rows=[{'concert':concert,'status':statuses.get(concert.pk,'-')} for concert in Concert.objects.order_by('date')]
    return render(request,'concerts.html',{'concerts':rows})

@login_required
def concert_detail(request,id):
    concert=get_object_or_404(Concert,pk=id)
    attending=concert.attendee.filter(user=request.user).first()
    return render(request,'concert_detail.html',{'concert_details':concert,'status':attending.attending if attending else '-','attending_choices':ConcertAttending.AttendingChoices.choices})

@login_required
@require_POST
def concert_attendee(request):
    concert=get_object_or_404(Concert,pk=request.POST.get('concert_id'))
    choice=request.POST.get('attendee_choice')
    if choice not in ConcertAttending.AttendingChoices.values:
        return HttpResponseBadRequest('Invalid RSVP choice')
    ConcertAttending.objects.update_or_create(concert=concert,user=request.user,defaults={'attending':choice})
    return redirect('concerts')
