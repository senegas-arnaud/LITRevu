from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from .forms import SignupForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows
from django.contrib import messages
from itertools import chain
from django.db.models import CharField, Value

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
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list('followed_user', flat=True)

    all_users = list(followed_users) + [request.user.pk]

    tickets = Ticket.objects.filter(
        user__in=all_users
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
        return redirect('my_post_ticket')

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
def review_answer_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    return render(request, 'review_answer.html', {'form': form, 'ticket': ticket})

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


User = get_user_model()

@login_required
def follow_view(request):
    following = UserFollows.objects.filter(user=request.user)
    
    if request.method == 'POST':
        unfollow_pk = request.POST.get('unfollow')
        if unfollow_pk:
            UserFollows.objects.filter(
                user=request.user,
                followed_user=unfollow_pk
            ).delete()
            return redirect('follow')

        username = request.POST.get('username')
        if username:
            try:
                user_to_follow = User.objects.get(username=username)
                if user_to_follow == request.user:
                    messages.error(request, 'Vous ne pouvez pas vous suivre vous même !')
                else:
                    UserFollows.objects.get_or_create(
                        user=request.user,
                        followed_user=user_to_follow
                    )
                    messages.success(request, f'Vous suivez maintenant {username} !')
            except User.DoesNotExist:
                messages.error(request, f"L'utilisateur {username} n'existe pas !")

    return render(request, 'follow.html', {'following': following})

@login_required
def ticket_reviews_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')

    return render(request, 'ticket_reviews.html', {
        'ticket': ticket,
        'reviews': reviews
    })