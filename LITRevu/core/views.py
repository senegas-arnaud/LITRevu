from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review

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
    logout(request)
    return redirect('login')

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
            return redirect('my_post_ticket')

    return render(request, 'ticket_edit.html', {'form': form})

@login_required
def ticket_delete_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        ticket.delete()
        return redirect('my_post')

    return render(request, 'ticket_delete.html', {'ticket': ticket})

@login_required
def review_create_view(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('home')

    return render(request, 'review_create.html', {'ticket_form': ticket_form,'review_form': review_form })

@login_required
def review_edit_view(request,pk):
    review = get_object_or_404(Review, pk=pk)
    form = ReviewForm(instance=review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('my_post_review')

    return render(request, 'review_edit.html', {'form': form})

@login_required
def review_delete_view(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review.delete()
        return redirect('my_post_review')

    return render(request, 'review_delete.html', {'review': review})

@login_required
def review_answer_view(request):
    return HttpResponse('')

@login_required
def my_post_ticket_view(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by('-time_created')
    
    return render(request, 'my_post_ticket.html', {'tickets': tickets })

@login_required
def my_post_review_view(request):
    reviews = Review.objects.filter(
        user=request.user
    ).order_by('-time_created')

    return render(request, 'my_post_review.html', {'reviews': reviews})


def follow_view(request):
    return HttpResponse('')