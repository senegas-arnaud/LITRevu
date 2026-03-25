from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket

def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'login.html', {'form': form})
    

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    return HttpResponse('')

@login_required
def home_view(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by('-time_created')
    
    return render(request, 'home.html', {'tickets': tickets})

@login_required
def ticket_create_view(request):
    form = TicketForm()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    return render(request, 'ticket_create.html', {'form': form})

@login_required
def ticket_edit_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('my-post')

    return render(request, 'ticket_edit.html', {'form': form})

@login_required
def ticket_delete_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        ticket.delete()
        return redirect('my_post')

    return render(request, 'ticket_delete.html', {'ticket': ticket})

def review_create_view(request):
    return HttpResponse('')

def review_edit_view(request):
    return HttpResponse('')

def review_delete_view(request):
    return HttpResponse('')

def review_answer_view(request):
    return HttpResponse('')

@login_required
def my_post_view(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by('-time_created')
    
    return render(request, 'my_post.html', {'tickets': tickets})

def follow_view(request):
    return HttpResponse('')