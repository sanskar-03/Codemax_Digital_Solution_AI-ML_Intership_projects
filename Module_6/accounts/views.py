from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def safe_next_url(request, default="home"):

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
    )

    if next_url:

        parsed = urlparse(next_url)

        if not parsed.netloc and next_url.startswith("/"):
            return next_url

    return default


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not username or not password:

            messages.error(
                request,
                "Please enter both username and password."
            )

        else:

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.username}."
                )

                return redirect(
                    safe_next_url(request)
                )

            messages.error(
                request,
                "The username or password is incorrect."
            )

    return render(
        request,
        "accounts/login.html",
        {
            "next": request.GET.get("next", "")
        }
    )


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = UserCreationForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            return redirect("home")

        messages.error(
            request,
            "Please correct the highlighted information."
        )

    for field in form.fields.values():

        field.widget.attrs["class"] = "field-control"

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def logout_view(request):

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been signed out successfully."
        )

    return redirect("landing")
