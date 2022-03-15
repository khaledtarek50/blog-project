from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, "your account has been created you are now able to login"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    current_user = request.user
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=current_user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=current_user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your Account Has Been Updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=current_user)
        profile_form = ProfileUpdateForm(instance=current_user.profile)
    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "users/profile.html", context)


def follow(request, user_id):
    if request.method == "POST":
        current_user = request.user
        if current_user is not None:
            user_to_follow = get_object_or_404(User, pk=user_id)
            current_user.follow(user_to_follow)
        else:
            messages.error(request, "please log in first sir")
            return redirect("login")
    return redirect(request.META["HTTP_REFERER"])


def unfollow(request, user_id):
    if request.method == "POST":
        current_user = request.user
        if current_user is not None:
            user_to_unfollow = get_object_or_404(User, pk=user_id)
            current_user.unfollow(user_to_unfollow)
        else:
            messages.error(request, "please log in first sir")
            return redirect("login")
    return redirect(request.META["HTTP_REFERER"])


def get_followers(request):
    if request.method == "GET":
        current_user = request.user
        if current_user is not None:
            followers = current_user.followers.all()
            context = {"followers": followers, "count": followers.count()}
            return render(request, "users/followers.html", context)
        else:
            messages.error(request, "please log in first sir")
            return redirect("login")


def get_following(request):
    if request.method == "GET":
        current_user = request.user
        if current_user is not None:
            following = current_user.following.all()
            context = {"following": following, "count": following.count()}
            return render(request, "users/following.html", context)
        else:
            messages.error(request, "please log in first sir")
            return redirect("login")
